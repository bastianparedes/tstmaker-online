import { Component, OnInit, inject } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import type { Exercise } from '../../types/Exercise';

@Component({
  selector: 'app-exercises',
  templateUrl: './exercises.component.html',
  standalone: true,
  imports: [MatTableModule, MatCheckboxModule, HttpClientModule],
})
export class ExercisesComponent implements OnInit {
  displayedColumns = ['id', 'name', 'description', 'dateModified', 'code'];
  exercises: Exercise[]  | undefined = undefined;
  httpClient = inject(HttpClient);

  ngOnInit() {
    this.httpClient.get('/api/exercises').subscribe((data) => {
      this.exercises = data as Exercise[];
    });
  }
}
