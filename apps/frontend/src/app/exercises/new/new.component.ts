import { Component } from '@angular/core';
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

const initialCode = `
def fn():
  n1 = Rational(1, 2)
  n2 = Rational(7, 5)

  return {
    comparator: {

    },
    alterantives: {
      'alternative_1': Rational(n1.get_numerator() + n2.get_numerator(), n1.get_denominator() + n2.get_denominator()),
      'alternative_2': Rational(n1.get_numerator() + n2.get_denominator(), n1.get_denominator() + n2.get_numerator()),
      'alternative_3': Rational(n1.get_denominator() + n2.get_numerator(), n1.get_numerator() + n2.get_denominator()),
      'alternative_4': n1 * n2,
      'alternative_5': n1 * n2 ** (-1)
    }
  }
`.trim();

@Component({
  selector: 'app-new-exercise',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule, // ¿no necesario?
    EditorComponent,
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
