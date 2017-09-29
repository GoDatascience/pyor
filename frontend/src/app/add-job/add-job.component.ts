import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl} from "@angular/forms";

import 'rxjs/add/operator/toPromise';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';
import {Task} from "../add-task/task";
import {MdDatepicker} from "@angular/material";
import {Http} from "@angular/http";


@Component({
  selector: 'app-add-job',
  templateUrl: './add-job.component.html',
  styleUrls: ['./add-job.component.css']
})
export class AddJobComponent implements OnInit {
  taskCtrl: FormControl;
  filtredTasks: any;
  tasks: Task[] = [];
  selectedTaskName: string;

  @ViewChild(MdDatepicker) picker: MdDatepicker<Date>;

  constructor(private http: Http) {
    this.taskCtrl = new FormControl();
  }

  ngOnInit(): void {
    this.getTasks().then(tasks => {
      console.log("construtor", tasks);
      this.tasks = tasks;
      this.filtredTasks = this.taskCtrl.valueChanges
        .startWith(null)
        .map(task => this.filterTasks(task));
    });

    console.log("tasks", this.tasks);
  }

  getTasks(): Promise<Task[]> {
    return this.http.get("http://localhost:5000/tasks")
      .toPromise()
      .then(response => response.json().items as Task[])
      .catch(AddJobComponent.handleError);
  }

  private static handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }

  filterTasks(taskName: string) {
    console.log("FilterTasks", this.tasks);
    return taskName ? this.tasks.filter(task =>
      task.name.toLowerCase().indexOf(taskName.toLowerCase()) > 0 ||
      task.name.toLowerCase().indexOf(taskName.toLowerCase()) === 0) : this.tasks;
  }

  loadParams(taskName: string) {
    console.log("Load params for", this.getTask(taskName));
  }

  getSelectedTask(): Task {
    return this.getTask(this.selectedTaskName);
  }

  getTask(taskName: string) {
    return this.tasks.filter(task => task.name === taskName)[0];
  }

  startJob() {
    console.log(this.getSelectedTask());
    console.log("Run....", this.getSelectedTask()._id);
    this.http.put("http://localhost:5000/tasks/" + this.getSelectedTask()._id, {
      queue: "sequential"
    }).toPromise()
      .then(response => console.log(response.json()))
      .catch(AddJobComponent.handleError);
  }
}
