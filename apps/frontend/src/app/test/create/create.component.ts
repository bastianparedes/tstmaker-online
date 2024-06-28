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

type Exercises = {
  id: number;
  name: string;
  quantity: number;
};

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
  ],
})
export class TestCreateComponent implements OnInit {
  isLoading = {
    initialLoad: true,
    creatingPdf: false,
  };
  isAtLeastOneExerciseSelectedWithQuantityNotZero = false;
  exercises = {
    unselected: [] as Exercises[],
    selected: [] as Exercises[],
  };
  httpClient = inject(HttpClient);
  classesPythonCode: string | undefined = undefined;
  pdfUrl: undefined | SafeResourceUrl = undefined;

  constructor(public sanitizer: DomSanitizer) {}

  async ngOnInit() {
    this.httpClient
      .get('/api/exercises?columns=id&columns=name')
      .subscribe((data) => {
        const exercises = (
          data as {
            id: number;
            name: string;
          }[]
        ).map((exercise) => {
          return {
            id: exercise.id,
            name: exercise.name,
            quantity: 0,
          };
        });
        this.exercises.unselected = exercises;
        this.isLoading.initialLoad = false;
      });
  }

  updateQuantity(id: number, event: Event) {
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
        const exercises: Promise<{
          statement: string;
          alternatives: string[];
        }>[] = [];
        exercisesPythonCodeData.forEach((exercisePythonCodeData) => {
          for (let i = 0; i < exercisePythonCodeData.quantity; i++) {
            const exercise = runPythonCode<{
              alternatives: string[];
              comparators: unknown[];
              identifiers: unknown[];
              statement: string;
            }>([classesPythonCode, exercisePythonCodeData.code].join('\n'));
            exercises.push(exercise);
          }
        });
        return Promise.all(exercises);
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
