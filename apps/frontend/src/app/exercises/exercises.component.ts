import {Component} from '@angular/core';
import {MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { ExerciseComponent } from './exercise/exercise.component';

const exercises = [
  {
    id: 0,
    name: 'Nombre 0',
    description: '',
    dateModified: 1712437097974,
    code: '',
  },
  {
    id: 1,
    name: 'Nombre 1',
    description: '',
    dateModified: 1712437097974,
    code: '',
  },
  {
    id: 2,
    name: 'Nombre 2',
    description: '',
    dateModified: 1712437097974,
    code: '',
  },
  {
    id: 3,
    name: 'Nombre 3',
    description: '',
    dateModified: 1712437097974,
    code: '',
  },
  {
    id: 4,
    name: 'Nombre 4',
    description: '',
    dateModified: 1712437097974,
    code: '',
  },
];

@Component({
  selector: 'app-exercises',
  templateUrl: './exercises.component.html',
  standalone: true,
  imports: [ExerciseComponent, MatTableModule, MatCheckboxModule],
})
export class ExercisesComponent {
  displayedColumns = ['id', 'name', 'description', 'dateModified', 'code'];
  exercises = exercises;
}
