import { Component, OnInit, Input, inject } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { EditorComponent } from '../common/editor/editor.component';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MonacoEditorModule } from 'ngx-monaco-editor-v2';
import { catchError, throwError } from 'rxjs';

type Exercise = {
  name: string;
  description: string;
  code: string;
};

@Component({
  selector: 'app-new-exercise',
  standalone: true,
  imports: [
    HttpClientModule,
    MatInputModule,
    MatFormFieldModule, // ¿no necesario?
    EditorComponent,
    MatButtonModule,
    FormsModule,
    ReactiveFormsModule,
    MonacoEditorModule,
  ],
  templateUrl: './edit.component.html',
})
export class ExerciseEditComponent implements OnInit {
  @Input() id!: string;
  exercise:
    | undefined
    | FormGroup<{
        name: FormControl<string | null>;
        description: FormControl<string | null>;
        code: FormControl<string | null>;
      }> = undefined;
  httpClient = inject(HttpClient);

  ngOnInit() {
    this.httpClient
      .get(
        `/api/exercises/${this.id}?columns=name&columns=description&columns=code`
      )
      .pipe(
        catchError(() => {
          location.href = '/exercises';
          return throwError(() => new Error('Element not found'));
        })
      )
      .subscribe((data) => {
        const typedData = data as Exercise;
        this.exercise = new FormGroup({
          name: new FormControl(typedData.name, [
            Validators.required,
            Validators.minLength(1),
          ]),
          description: new FormControl(typedData.description, [
            Validators.required,
            Validators.minLength(1),
          ]),
          code: new FormControl(typedData.code, [
            Validators.required,
            Validators.minLength(1),
          ]),
        });
      });
  }

  async save(event: SubmitEvent) {
    event.preventDefault();
    if (this.exercise === undefined || !this.exercise.valid) return;
    console.log(this.exercise.value);

    const response = await fetch(`/api/exercises/${this.id}`, {
      body: JSON.stringify(this.exercise.value),
      headers: {
        'Content-Type': 'application/json',
      },
      method: 'PUT',
    });

    if (response.ok) location.href = '/exercises';
  }
}
