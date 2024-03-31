import { Component } from '@angular/core';
import { ExercisesComponent } from './exercises/exercises.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ExercisesComponent],
  templateUrl: './app.component.html'
})
export class AppComponent {
  title = 'frontend';
  toggleValue = true;
  toggleChanged() {
    console.log('TOGGLE CLICK');
  }
}
