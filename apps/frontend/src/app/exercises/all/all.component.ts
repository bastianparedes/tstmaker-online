import { Component, OnInit, inject } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import type { Exercise } from '../../../types/Exercise';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-exercises-all',
  templateUrl: './all.component.html',
  standalone: true,
  imports: [MatTableModule, MatCheckboxModule, HttpClientModule, MatIconModule],
})
export class ExercisesAllComponent implements OnInit {
  displayedColumns = [
    'id',
    'name',
    'description',
    'last_modified_date',
    'code',
  ];
  exercises: Exercise[] | undefined = undefined;
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
}
