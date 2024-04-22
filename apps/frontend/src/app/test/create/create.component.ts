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

type Exercise = {
  id: number;
  name: string;
  code: string;
  description: string;
  last_modified_date: string;
};

@Component({
  selector: 'app-test-create',
  templateUrl: './create.component.html',
  styleUrl: './create.component.css',
  standalone: true,
  imports: [CdkDropList, CdkDrag, HttpClientModule, MatButtonModule],
})
export class TestCreateComponent implements OnInit {
  exercises: Exercise[] | undefined = undefined;
  exercisesSelected: Exercise[] = [];

  httpClient = inject(HttpClient);

  ngOnInit() {
    this.httpClient.get('/api/exercises').subscribe((data) => {
      this.exercises = data as Exercise[];
      this.exercises.forEach((exercise) => {
        const date = new Date(exercise.last_modified_date);
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        exercise.last_modified_date = `${day}/${month}/${year}`;
      });
    });
  }

  drop(event: CdkDragDrop<Exercise[]>) {
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
