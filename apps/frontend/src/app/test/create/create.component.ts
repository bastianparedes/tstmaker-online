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
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';


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
  exercises: ExerciseWithQuantity[] | undefined = undefined;
  exercisesSelected: ExerciseWithQuantity[] = [
    {
      id: 0,
      name: 'Primero ejercicio',
      quantity: 5,
    },
  ];

  httpClient = inject(HttpClient);

  ngOnInit() {
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

  createTest() {
    console.log(this.exercisesSelected);
  }
}
