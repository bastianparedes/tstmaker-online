import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { MonacoEditorModule } from 'ngx-monaco-editor-v2';

@Component({
  selector: 'app-editor',
  standalone: true,
  imports: [FormsModule, MonacoEditorModule],
  templateUrl: './editor.component.html',
})
export class EditorComponent {
  @Input() code = '';

  onChange(newCode: string) {
    this.code = newCode;
  }
}
