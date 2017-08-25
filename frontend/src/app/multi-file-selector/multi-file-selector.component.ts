import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-multi-file-selector',
  templateUrl: './multi-file-selector.component.html',
  styleUrls: ['./multi-file-selector.component.css']
})
export class MultiFileSelectorComponent implements OnInit {
  private _files: File[] = [];

  constructor() { }

  ngOnInit() {
  }

  onFileSelect(fileList: File[]) {
    for(let file of fileList) {
      this._files.push(file);
    }

    console.log(this._files);
  }

  removeFile(file) {
    let index = this._files.indexOf(file, 0);

    if (index > -1) {
      this._files.splice(index, 1);
    }
  }

}
