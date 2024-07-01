import { Component, OnInit, inject } from '@angular/core';
import {
  CdkDragDrop,
  moveItemInArray,
  transferArrayItem,
  CdkDrag,
  CdkDropList,
} from '@angular/cdk/drag-drop';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { runPythonCode } from '../../utils/pyscript';
import { completeLatexCode, tableUniqueSelection } from '../../utils/latex';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { LoaderComponent } from '../../common/loader/loader.component';
import { everyElementIsDifferent, arrayIncludesElement } from '../../utils/array';
import { MatPaginatorModule } from '@angular/material/paginator';
import type { PageEvent } from '@angular/material/paginator';

interface Exercises {
  id: number;
  name: string;
  description: string;
  quantity: number;
}

@Component({
  selector: 'app-test-create',
  templateUrl: './create.component.html',
  styleUrl: './create.component.css',
  standalone: true,
  imports: [
    CdkDropList,
    CdkDrag,
    HttpClientModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    LoaderComponent,
    MatPaginatorModule
  ],
})
export class TestCreateComponent implements OnInit {
  isLoading = {
    fetchingExercises: true,
    creatingPdf: false,
  };
  filters = {
    query: '',
    itemsPerPage: 100,
    itemsPerOptions: [10, 25, 50, 100],
    page: 0,
    totalPages: 1,
    totalExercises: 0,
  };
  queryTimeout = NaN;
  isAtLeastOneExerciseSelectedWithQuantityNotZero = false;
  exercises = {
    unselected: [] as Exercises[],
    selected: [] as Exercises[],
  };
  httpClient = inject(HttpClient);
  classesPythonCode: string | undefined = undefined;
  pdfUrl: undefined | SafeResourceUrl = undefined;

  constructor(public sanitizer: DomSanitizer) {}

  fetchExercises(query: string, page: number, pageSize: number) {
    this.isLoading.fetchingExercises = true;

    const queryParams = new URLSearchParams();
    queryParams.append('columns', 'id');
    queryParams.append('columns', 'name');
    queryParams.append('columns', 'description');
    queryParams.append('columns', 'last_modified_date');
    queryParams.append('query', query);
    queryParams.append('page_number', String(page));
    queryParams.append('items_per_page', String(pageSize));
    this.httpClient
      .get(
        `/api/exercises?${queryParams.toString()}`
      )
      .subscribe((data) => {
        const typedData = data as {
          exercises: {
            id: number;
            name: string;
            description: string;
          }[];
          total: number;
        };

        const exercises = typedData.exercises.map((exercise) => {
          return {
            ...exercise,
            quantity: 0,
          };
        });
        this.filters.totalExercises = typedData.total;

        const usedIds = this.exercises.selected.map((exercise) => exercise.id);
        this.exercises.unselected = exercises.filter((exercise) => !usedIds.includes(exercise.id));

        this.filters.page = page;
        this.filters.itemsPerPage = pageSize;
        this.filters.totalExercises = typedData.total;
        this.isLoading.fetchingExercises = false;
      });
  }

  async ngOnInit() {
    this.fetchExercises(this.filters.query, this.filters.page, this.filters.itemsPerPage);
  }

  handleQueryInput(event: Event) {
    this.filters.query = (event.target as HTMLInputElement).value;
    clearTimeout(this.queryTimeout);
    this.queryTimeout = Number(setTimeout(() => {
      this.fetchExercises(this.filters.query, 0, this.filters.itemsPerPage);
    }, 1000));
  }

  handlePageEvent(event: PageEvent) {
    this.fetchExercises(this.filters.query, event.pageIndex, event.pageSize);
  }

  updateQuantityWithKeyboard(event: KeyboardEvent) {
    if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') event.preventDefault();
  }

  updateQuantity(event: Event, id: number) {
    const exercise = this.exercises.selected.find(
      (exerciseInList) => exerciseInList.id === id
    );
    if (exercise === undefined) return;
    exercise.quantity = Number((event.target as HTMLInputElement).value);
    this.isAtLeastOneExerciseSelectedWithQuantityNotZero =
      this.exercises.selected.some((exercise) => exercise.quantity > 0);
  }

  drop(event: CdkDragDrop<Exercises[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    } else {
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }

  async createTest() {
    this.isLoading.creatingPdf = true;
    const exercisesSelected = this.exercises.selected.filter(
      (exercise) => exercise.quantity > 0
    );
    const classesPythonCodePromise = new Promise<string>((resolve) => {
      if (this.classesPythonCode !== undefined)
        return resolve(this.classesPythonCode);
      this.httpClient
        .get('/api/classes', { responseType: 'text' })
        .subscribe((data) => {
          this.classesPythonCode = data;
          resolve(data);
        });
    });

    const exercisesPythonCodeDataPromise = new Promise<
      {
        id: number;
        code: string;
        quantity: number;
      }[]
    >((resolve) => {
      const queryParams = new URLSearchParams();
      queryParams.append('columns', 'id');
      queryParams.append('columns', 'code');
      exercisesSelected.forEach((exerciseSelected) =>
        queryParams.append('ids', String(exerciseSelected.id))
      );
      this.httpClient
        .get<
          {
            id: number;
            code: string;
          }[]
        >(`/api/exercises?${queryParams.toString()}`)
        .subscribe((exercises) => {
          const completeDatas: {
            id: number;
            code: string;
            quantity: number;
          }[] = [];
          for (const exercise of exercises) {
            const quantity = exercisesSelected.find(
              (exerciseSelected) => exerciseSelected.id === exercise.id
            )?.quantity;
            if (quantity === undefined) continue;
            completeDatas.push({
              ...exercise,
              quantity: quantity,
            });
          }
          resolve(completeDatas);
        });
    });
    Promise.all([classesPythonCodePromise, exercisesPythonCodeDataPromise])
      .then(async ([classesPythonCode, exercisesPythonCodeData]) => {
        const exercises: {
          statement: string;
          alternatives: string[];
        }[] = [];
        for (const exercisePythonCodeData of exercisesPythonCodeData) {
          const identifiersUsed: unknown[] = [];
          for (let i = 0; i < exercisePythonCodeData.quantity; i++) {
            for (let tryCount = 0 ; tryCount < 30 ; tryCount++) {
              const exercise = await runPythonCode<{
                alternatives: string[];
                comparators: unknown[];
                identifiers: unknown;
                statement: string;
              } | undefined>([classesPythonCode, exercisePythonCodeData.code].join('\n'));
              if (exercise === undefined) continue;
              if (everyElementIsDifferent(exercise.comparators)) continue;
              if (arrayIncludesElement(identifiersUsed, exercise.identifiers)) continue;

              identifiersUsed.push(exercise.identifiers);
              exercises.push(exercise);
              break;
            }
            
          }
        }
        return exercises;
      })
      .then((result) => completeLatexCode(tableUniqueSelection(result)))
      .then((latexCode) => {
        return fetch('/api/pdf_url', {
          body: JSON.stringify({
            latex_code: latexCode,
          }),
          headers: {
            'Content-Type': 'application/json',
          },
          method: 'POST',
        });
      })
      .then((response) => response.text())
      .then((pdfUrl) => {
        this.pdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(pdfUrl);
      })
      .finally(() => {
        this.isLoading.creatingPdf = false;
      });
  }
}
