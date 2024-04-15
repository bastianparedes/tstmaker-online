import { Component } from '@angular/core';
import { ExercisesComponent } from './exercises/exercises.component';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ExercisesComponent, RouterOutlet],
  templateUrl: './app.component.html'
})
export class AppComponent {
}
