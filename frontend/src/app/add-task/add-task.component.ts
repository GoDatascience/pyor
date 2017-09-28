import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Component({
  selector: 'app-add-task',
  templateUrl: './add-task.component.html',
  styleUrls: ['./add-task.component.css']
})
export class AddTaskComponent implements OnInit {
  parameters: Parameter[] = [];
  scriptFile: File;
  taskName: string;
  types: string[] = ["text", "number", "date", "boolean"];

  constructor(private http: HttpClient) {
  }

  ngOnInit() {
  }

  addTask(): void {
    const headers = new HttpHeaders();

    //headers.set('Content-Type', 'application/x-www-form-urlencoded');
    headers.set('enctype', 'multipart/form-data');

    let body = new FormData();

    const data = {
      name: this.taskName
    };

    body.append('script_file', this.scriptFile);
    body.append('data', JSON.stringify(data));

    this.http.post("http://localhost:5000/tasks", body, {headers: headers}).subscribe(data => {
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
