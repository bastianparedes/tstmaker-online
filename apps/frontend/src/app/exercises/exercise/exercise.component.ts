import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-exercise',
  standalone: true,
  imports: [],
  templateUrl: './exercise.component.html',
})
export class ExerciseComponent implements OnInit {
  @Input({ required: true }) id!: number;
  @Input({ required: true }) name!: string;
  @Input({ required: true }) description!: string;
  @Input({ required: true }) last_modified_date!: string;
  @Input({ required: true }) code!: string;
  date: string | undefined;

  constructor() {
    console.log('AYUDA CONSTRUCTOR');
  }

  ngOnInit() {
    console.log('AYUDA ONINIT');
    const date = new Date(this.last_modified_date)
    this.date = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
  }

  handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    console.log({ id: this.id, name: this.name })
  }
}
