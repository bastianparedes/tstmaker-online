import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

import { MonacoEditorModule } from 'ngx-monaco-editor-v2';

import 'zone.js';

@Component({
  selector: 'app-editor',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    FormsModule,
    ReactiveFormsModule,
    MonacoEditorModule,
  ],
  templateUrl: './editor.component.html',
})
export class EditorComponent {
  @Input() code = '';

  updateCode(newCode: string) {
    console.log(newCode);
  }

  onChange(event: Event) {
    const target = event.target as HTMLTextAreaElement;
    const code = target.value;
    console.log(code);
    this.code = code;
  }
}
