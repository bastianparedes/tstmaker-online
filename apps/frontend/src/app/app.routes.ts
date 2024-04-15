import type { Routes } from '@angular/router';
import { ExercisesComponent } from './exercises/exercises.component';
import { ExerciseComponent } from './exercise/exercise.component';

export const routes: Routes = [
  { path: 'exercises', component: ExercisesComponent },
  { path: 'exercise', component: ExerciseComponent },
];
