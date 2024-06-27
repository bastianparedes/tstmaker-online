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

type Exercise = {
  id: number;
  name: string;
};

type ExerciseWithQuantity = Exercise & {
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
  ],
})
export class TestCreateComponent implements OnInit {
  exercises: ExerciseWithQuantity[] = [];
  exercisesSelected: ExerciseWithQuantity[] = [];
  isLoading = true;
  httpClient = inject(HttpClient);
  classesPythonCode: string | undefined = undefined;

  async ngOnInit() {
    this.httpClient
      .get('/api/exercises?columns=id&columns=name')
      .subscribe((data) => {
        this.exercises = (data as Exercise[]).map((exercise) => {
          return {
            ...exercise,
            quantity: 0,
          };
        });
      });
  }

  drop(event: CdkDragDrop<ExerciseWithQuantity[]>) {
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
      this.exercisesSelected.forEach((exerciseSelected) =>
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
            const quantity = this.exercisesSelected.find(
              (exerciseSelected) => exerciseSelected.id === exercise.id
            )?.quantity;
            if (quantity === undefined) continue;
            completeDatas.push({
              ...exercise,
              quantity,
            });
          }
          resolve(completeDatas);
        });
    });

    const [classesPythonCode, exercisesPythonCodeData] = await Promise.all([
      classesPythonCodePromise,
      exercisesPythonCodeDataPromise,
    ]);

    const result = await Promise.all(
      exercisesPythonCodeData.map((exercisePythonCodeData) => {
        return runPythonCode(
          [classesPythonCode, exercisePythonCodeData.code].join('\n')
        );
      })
    );
  }
}
