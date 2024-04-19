import { Component, OnInit, Input, inject } from '@angular/core';
import type { Exercise } from '../../../types/Exercise';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { EditorComponent } from '../common/editor/editor.component';
import {
  FormsModule,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

@Component({
  selector: 'app-edit-exercise',
  standalone: true,
  imports: [
    HttpClientModule,
    MatInputModule,
    MatFormFieldModule,
    EditorComponent,
    MatButtonModule,
    FormsModule,
  ],
  templateUrl: './edit-exercise.component.html',
})
export class EditExerciseComponent implements OnInit {
  @Input() id!: string;
  exercise: Exercise | undefined = undefined;
  httpClient = inject(HttpClient);

  form = new FormGroup({
    name: new FormControl('Name', [
      Validators.required,
      Validators.minLength(0),
    ]),
    description: new FormControl('Name', [
      Validators.required,
      Validators.minLength(0),
    ]),
    code: new FormControl('Code', [
      Validators.required,
      Validators.minLength(0),
    ]),
  });

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

  updateName(newName: string) {
    if (this.exercise === undefined) return;
    this.exercise.name = newName;
  }

  updateDescription(newDescription: string) {
    if (this.exercise === undefined) return;
    this.exercise.description = newDescription;
  }

  updateCode(newCode: string) {
    if (this.exercise === undefined) return;
    this.exercise.code = newCode;
  }

  save(event: SubmitEvent) {
    event.preventDefault();
    console.log('SUBMIT', this.exercise);
  }
}
