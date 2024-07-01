import { Component, OnInit, inject } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatIconModule } from '@angular/material/icon';
import { MatPaginatorModule } from '@angular/material/paginator';
import type { PageEvent } from '@angular/material/paginator';
import { LoaderComponent } from '../common/loader/loader.component';
import { MatInputModule } from '@angular/material/input';


interface Exercise {
  id: number;
  name: string;
  description: string;
  last_modified_date: string;
}

@Component({
  selector: 'app-exercises',
  templateUrl: './exercises.component.html',
  standalone: true,
  imports: [MatTableModule, MatCheckboxModule, HttpClientModule, MatIconModule, MatPaginatorModule, LoaderComponent, MatInputModule],
})
export class ExercisesComponent implements OnInit {
  isLoading = true;
  displayedColumns = [
    'id',
    'name',
    'description',
    'last_modified_date',
    'code',
  ];
  exercises: Exercise[] | undefined = undefined;
  httpClient = inject(HttpClient);
  filters = {
    query: '',
    itemsPerPage: 25,
    itemsPerOptions: [10, 25, 50, 100],
    page: 0,
    totalPages: 1,
    totalExercises: 0,
  };
  queryTimeout = NaN;

  fetchExercises(query: string, page: number, pageSize: number) {
    this.isLoading = true;

    const queryParams = new URLSearchParams();
    queryParams.append('columns', 'id');
    queryParams.append('columns', 'name');
    queryParams.append('columns', 'description');
    queryParams.append('columns', 'last_modified_date');
    queryParams.append('query', query);
    queryParams.append('page_number', String(page));
    queryParams.append('items_per_page', String(pageSize));
    this.httpClient
      .get(
        `/api/exercises?${queryParams.toString()}`
      )
      .subscribe((data) => {
        const typedData = data as {
          exercises: Exercise[];
          total: number;
        };
        this.exercises = typedData.exercises;
        this.exercises.forEach((exercise) => {
          const date = new Date(exercise.last_modified_date);
          const day = date.getDate();
          const month = date.getMonth() + 1;
          const year = date.getFullYear();
          exercise.last_modified_date = `${day}/${month}/${year}`;
        });

        this.filters.page = page;
        this.filters.itemsPerPage = pageSize;
        this.filters.totalExercises = typedData.total;
        this.isLoading = false;
      });
  }

  ngOnInit() {
    this.fetchExercises(this.filters.query, this.filters.page, this.filters.itemsPerPage);
  }

  handlePageEvent(event: PageEvent) {
    this.fetchExercises(this.filters.query, event.pageIndex, event.pageSize);
  }

  handleQueryInput(event: Event) {
    this.filters.query = (event.target as HTMLInputElement).value;
    clearTimeout(this.queryTimeout);
    this.queryTimeout = Number(setTimeout(() => {
      this.fetchExercises(this.filters.query, 0, this.filters.itemsPerPage);
    }, 1000));
  }
}
