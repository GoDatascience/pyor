import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MRQDashboardComponent } from './mrq-dashboard.component';

describe('MRQDashboardComponent', () => {
  let component: MRQDashboardComponent;
  let fixture: ComponentFixture<MRQDashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MRQDashboardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MRQDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
