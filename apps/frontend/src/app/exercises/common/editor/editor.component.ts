import { CommonModule } from '@angular/common';
import { Component, importProvidersFrom } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { RouterOutlet } from '@angular/router';

import { MonacoEditorModule } from 'ngx-monaco-editor-v2';
import * as monaco from 'monaco-editor';

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
  private _editor?: any;
  name = 'Angular';
  public editorOptions = {
    theme: 'vs-light',
    language: 'python',
    wordWrap: 'on',
    automaticLayout: true,
    value: 'hols',
  };
  public text: FormControl<string>;
  public form: FormGroup;
  public myGroup: any;

  constructor(formBuilder: FormBuilder) {
    this.text = formBuilder.control('', { nonNullable: true });
    this.form = formBuilder.group({ text: this.text });
  }

  public onEditorInit(editor: monaco.editor.IStandaloneCodeEditor) {
    this._editor = editor;
    editor.focus();
  }

  public onChange(event: any) {
    console.log(event.target.value);
  }
}
