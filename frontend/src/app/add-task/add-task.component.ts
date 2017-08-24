import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-add-task',
  templateUrl: './add-task.component.html',
  styleUrls: ['./add-task.component.css']
})
export class AddTaskComponent implements OnInit {
  parameters: Parameter[] = [];
  scriptFileName: string;
  types: string[] = ["text", "number", "date", "boolean"];

  constructor() {
  }

  ngOnInit() {
  }

  addTask(): void {

  }

  addParam(): void {
    this.parameters.push(new Parameter("New Parameter", "text"));
  }

  removeParam(parameter: Parameter): void {
    let index = this.parameters.indexOf(parameter, 0);

    if (index > -1) {
      this.parameters.splice(index, 1);
    }
  }

  onFileSelect(fileList) {
    this.scriptFileName = fileList[0].name;
  }

}

export class Parameter {
  constructor(private name: string, private type: string) {
  }
}
