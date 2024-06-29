import { Component } from '@angular/core';
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

const initialCode = `
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
  selector: 'app-new-exercise',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule, // ¿no necesario?
    MatButtonModule,
    FormsModule,
    ReactiveFormsModule,
    MonacoEditorModule,
  ],
  templateUrl: './new.component.html',
})
export class ExerciseNewComponent {
  exercise = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.minLength(1)]),
    description: new FormControl('', [
      Validators.required,
      Validators.minLength(1),
    ]),
    code: new FormControl(initialCode, [
      Validators.required,
      Validators.minLength(1),
    ]),
  });

  async save(event: SubmitEvent) {
    event.preventDefault();
    if (!this.exercise.valid) return;

    const response = await fetch('/api/exercises', {
      body: JSON.stringify(this.exercise.value),
      headers: {
        'Content-Type': 'application/json',
      },
      method: 'POST',
    });

    if (response.ok) location.href = '/exercises';
  }
}
