import { Component } from '@angular/core';
import { ExercisesComponent } from './exercises/exercises.component';
import { RouterOutlet } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ExercisesComponent, RouterOutlet, MatIconModule],
  templateUrl: './app.component.html'
})
export class AppComponent {
}
