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

const defaultCode = `
def fn():
  n1_numerator = random.randint(1, 12)
  n1_denominator = random.randint(1, 12)
  n2_numerator = random.randint(2, 12)
  n2_denominator = random.randint(2, 12)

  n1 = Rational(n1_numerator, n1_denominator).simplify()
  n2 = Rational(n2_numerator, n2_denominator).simplify()

  # Obliga que las fracciones tengan distintos denominadores y estos sean distintos de 1
  if not (n1.get_denominator() != n2.get_denominator() and n1.get_denominator() != 1 and n2.get_denominator() != 1):
    return;

  math_expression = Latex.math_mode(f'{n1} + {n2}')

  return {
    'statement': f'¿Cuál es el resultado de {math_expression}?',
    'alternatives': [
      Latex.math_mode(n1 + n2), # Esta debe ser la respuesta correcta
      Latex.math_mode(Rational(n1.get_numerator() + n2.get_denominator(), n1.get_denominator() + n2.get_numerator())),
      Latex.math_mode(Rational(n1.get_denominator() + n2.get_numerator(), n1.get_numerator() + n2.get_denominator())),
      Latex.math_mode(n1 * n2),
      Latex.math_mode(n1 * n2 ** (-1))
    ],
    'comparators': [
      float(n1 + n2),
      float(Rational(n1.get_numerator() + n2.get_denominator(), n1.get_denominator() + n2.get_numerator())),
      float(Rational(n1.get_denominator() + n2.get_numerator(), n1.get_numerator() + n2.get_denominator())),
      float(n1 * n2),
      float(n1 * n2 ** (-1))
    ],
    'identifiers': [n1.get_numerator(), n1.get_denominator(), n2.get_numerator(), n2.get_numerator()]
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

    const queryParams = new URLSearchParams();
    queryParams.append('columns', 'name');
    queryParams.append('columns', 'description');
    queryParams.append('columns', 'code');
    this.httpClient
      .get(
        `/api/exercises/${this.id}?${queryParams.toString()}`
      )
      .pipe(
        catchError(() => {
          location.href = '/exercises';
          return throwError(() => new Error('Element not found'));
        })
      )
      .subscribe((data) => {
        
        const typedData = data as {
          name: string;
          description: string;
          code: string;
        };
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

    // if (this.isNewExercise) {
    //   for (let i = 0; i < 1000 ; i++) {
    //     await fetch(url, {
    //       body: JSON.stringify(this.exercise.value),
    //       headers: {
    //         'Content-Type': 'application/json',
    //       },
    //       method: this.isNewExercise ? 'POST' : 'PUT',
    //     });
    //   }
    // }


    location.href = '/exercises';
  }
}
