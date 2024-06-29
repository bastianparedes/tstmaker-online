import type { Routes } from '@angular/router';
import { ExerciseComponent } from './exercise/exercise.component';
import { ExercisesComponent } from './exercises/exercises.component';
import { TestCreateComponent } from './test/create/create.component';

export const routes: Routes = [
  { path: 'exercises', component: ExercisesComponent },
  { path: 'exercise', component: ExerciseComponent },
  { path: 'exercise/:id', component: ExerciseComponent },
  { path: 'test/create', component: TestCreateComponent },
  { path: '', redirectTo: 'exercises', pathMatch: 'full' },
];
