import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-exercise',
  standalone: true,
  imports: [],
  templateUrl: './exercise.component.html',
})
export class ExerciseComponent {
  @Input({ required: true }) id!: number;
  @Input({ required: true }) name!: string;
  @Input({ required: true }) description!: string;
  @Input({ required: true }) dateModified!: number;
  @Input({ required: true }) code!: string;

  handleSubmit() {
    console.log({ id: this.id, name: this.name })
  }
}
