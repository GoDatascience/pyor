import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-add-task',
  templateUrl: './add-task.component.html',
  styleUrls: ['./add-task.component.css']
})
export class AddTaskComponent implements OnInit {
  parameters: Parameter[] = [];
  scriptFile: File;
  types: string[] = ["text", "number", "date", "boolean"];

  constructor(private http: HttpClient) {
  }

  ngOnInit() {
  }

  addTask(): void {
    let headers = {
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Origin': '*',
      "enctype": "multipart/form-data"
    };

    this.http.post("http://localhost:5000/tasks",
      {
        headers: headers,
        data: {
          name: "Task teste"
        }
      }).subscribe(data => {
      console.log("Post realizado");
      console.log(data);
    });
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
    this.scriptFile = fileList[0];
  }

}

export class Parameter {
  constructor(private name: string, private type: string) {
  }
}
