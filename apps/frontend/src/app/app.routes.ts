import type { Routes } from '@angular/router';
import { AllExercisesComponent } from './exercises/all-exercises/all-exercises.component';
import { EditExerciseComponent } from './exercises/edit-exercise/edit-exercise.component';
import { NewExerciseComponent } from './exercises/new-exercise/new-exercise.component';

export const routes: Routes = [
  { path: 'exercises', component: AllExercisesComponent },
  { path: 'exercises/edit/:id', component: EditExerciseComponent },
  { path: 'exercises/new', component: NewExerciseComponent },
];
