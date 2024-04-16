import { Component, OnInit, Input, inject } from '@angular/core';
import type { Exercise } from '../../../types/Exercise';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { catchError, throwError } from 'rxjs';

@Component({
  selector: 'app-edit-exercise',
  standalone: true,
  imports: [HttpClientModule, RouterLink],
  templateUrl: './edit-exercise.component.html',
})
export class EditExerciseComponent implements OnInit {
  @Input() id!: string;
  exercise: Exercise  | undefined = undefined;
  httpClient = inject(HttpClient)

  ngOnInit() {
    this.httpClient.get(`/api/exercises/${this.id}`)
      .pipe(
        catchError(() => {
          location.href = '/exercises';
          return throwError(() => new Error('Element not found'));
        })
      )
      .subscribe((data) => {
        this.exercise = data as Exercise;
      });
  }
}
