import { Component } from '@angular/core';
import { EditorComponent } from '../common/editor/editor.component';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';

const initialCode = `
def fn():
  n1 = Rational(1, 2)
  n2 = Rational(7, 5)

  return {
    'alternative_1': Rational(n1.get_numerator() + n2.get_numerator(), n1.get_denominator() + n2.get_denominator),
    'alternative_2': Rational(n1.get_numerator() + n2.get_denominator(), n1.get_denominator() + n2.get_numerator),
    'alternative_3': Rational(n1.get_denominator() + n2.get_numerator(), n1.get_numerator() + n2.get_denominator),
    'alternative_4': n1 * n2,
    'alternative_5': n1 * n2 ** (-1)
  }
`;

@Component({
  selector: 'app-new-exercise',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule, // ¿no necesario?
    EditorComponent,
    MatButtonModule,
    FormsModule,
  ],
  templateUrl: './new-exercise.component.html',
})
export class NewExerciseComponent {
  exercise = {
    name: '',
    description: '',
    code: initialCode,
  };

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
