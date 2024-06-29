import { Component, OnInit, Input, inject } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
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

interface Exercise {
  name: string;
  description: string;
  code: string;
}

const defaultCode = `
def fn():
  n1_numerator = random.randint(1, 10)
  n1_denominator = random.randint(1, 10)
  n2_numerator = random.randint(2, 10)
  n2_denominator = random.randint(2, 10)

  n1 = Rational(n1_numerator, n1_denominator).simplify()
  n2 = Rational(n2_numerator, n2_denominator).simplify()

  math_expression = Latex.math_mode(f'{n1} + {n2}')

  return {
    'statement': f'¿Cuál es el resultado de {math_expression}?',
    'alternatives': [
      Latex.math_mode(n1 + n2), # this is must be the correct one
      Latex.math_mode(Rational(n1.get_numerator() + n2.get_denominator(), n1.get_denominator() + n2.get_numerator())),
      Latex.math_mode(Rational(n1.get_denominator() + n2.get_numerator(), n1.get_numerator() + n2.get_denominator())),
      Latex.math_mode(n1 * n2),
      Latex.math_mode(n1 * n2 ** (-1))
    ],
    'comparators': [
      n1 + n2,
      Rational(n1.get_numerator() + n2.get_denominator(), n1.get_denominator() + n2.get_numerator()),
      Rational(n1.get_denominator() + n2.get_numerator(), n1.get_numerator() + n2.get_denominator()),
      n1 * n2,
      n1 * n2 ** (-1)
    ],
    'identifiers': [n1, n2]
  }
`.trim();

@Component({
  selector: 'app-exercise',
  standalone: true,
  imports: [
    HttpClientModule,
    MatInputModule,
    MatFormFieldModule, // ¿no necesario?
    MatButtonModule,
    FormsModule,
    ReactiveFormsModule,
    MonacoEditorModule,
  ],
  templateUrl: './exercise.component.html',
})
export class ExerciseComponent implements OnInit {
  @Input() id!: undefined | string;
  exercise =  new FormGroup({
    name: new FormControl('', [
      Validators.required,
      Validators.maxLength(100),
    ]),
    description: new FormControl('', [
      Validators.required,
      Validators.minLength(1),
      Validators.maxLength(100),
    ]),
    code: new FormControl(defaultCode, [
      Validators.required,
      Validators.minLength(1),
    ]),
  });
  isNewExercise!: boolean;
  httpClient = inject(HttpClient);

  ngOnInit() {
    this.isNewExercise = this.id === undefined;
    if (this.isNewExercise) {
      this.exercise.setValue({
        name: '',
        description: '',
        code: defaultCode
      });

      return;
    }

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
        this.exercise.setValue({
          name: typedData.name,
          description: typedData.description,
          code: typedData.code
        });
      });
  }

  async save(event: SubmitEvent) {
    event.preventDefault();
    if (!this.exercise.valid) return;

    const url = this.isNewExercise ? '/api/exercises' : `/api/exercises/${this.id}`
    await fetch(url, {
      body: JSON.stringify(this.exercise.value),
      headers: {
        'Content-Type': 'application/json',
      },
      method: this.isNewExercise ? 'POST' : 'PUT',
    });

    location.href = '/exercises';
  }
}
