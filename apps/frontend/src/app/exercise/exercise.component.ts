import { Component, OnInit, inject } from '@angular/core';
import type { Exercise } from '../../types/Exercise';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-exercise',
  standalone: true,
  imports: [HttpClientModule],
  templateUrl: './exercise.component.html',
})
export class ExerciseComponent {
  exercise: Exercise  | undefined = undefined;
  httpClient = inject(HttpClient)

  ngOnInit() {
    this.httpClient.get('/api/exercises/20').subscribe((data) => {
      this.exercise = data as Exercise;
    });
  }
}
