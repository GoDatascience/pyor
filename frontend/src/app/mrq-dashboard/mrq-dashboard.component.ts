import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-mrq-dashboard',
  templateUrl: './mrq-dashboard.component.html',
  styleUrls: ['./mrq-dashboard.component.css']
})
export class MRQDashboardComponent implements OnInit {
  el: HTMLFrameElement;

  constructor() {
  }

  ngOnInit() {
  }

  onload(ev: Event) {
    this.el = <HTMLFrameElement>ev.srcElement;
    this.adjust();
  }

  adjust() {
    this.el.height = window.innerHeight;
    this.el.width = "100%";
  }

}
