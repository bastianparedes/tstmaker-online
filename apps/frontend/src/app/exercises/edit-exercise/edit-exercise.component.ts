import { Component, OnInit, Input, inject } from '@angular/core';
import type { Exercise } from '../../../types/Exercise';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { EditorComponent } from '../common/editor/editor.component';

@Component({
  selector: 'app-edit-exercise',
  standalone: true,
  imports: [
    HttpClientModule,
    MatInputModule,
    MatFormFieldModule,
    EditorComponent,
  ],
  templateUrl: './edit-exercise.component.html',
})
export class EditExerciseComponent implements OnInit {
  @Input() id!: string;
  exercise: Exercise | undefined = undefined;
  httpClient = inject(HttpClient);

  ngOnInit() {
    this.httpClient
      .get(`/api/exercises/${this.id}`)
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

  save(event: SubmitEvent) {
    event.preventDefault();
    console.log('SUBMIT', this.exercise);
  }
}
