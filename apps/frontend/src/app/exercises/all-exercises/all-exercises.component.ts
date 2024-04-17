import { Component, OnInit, inject } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import type { Exercise } from '../../../types/Exercise';

@Component({
  selector: 'app-all-exercises',
  templateUrl: './all-exercises.component.html',
  standalone: true,
  imports: [MatTableModule, MatCheckboxModule, HttpClientModule],
})
export class AllExercisesComponent implements OnInit {
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
      console.log(data);
      this.exercises = data as Exercise[];
    });
  }
}
