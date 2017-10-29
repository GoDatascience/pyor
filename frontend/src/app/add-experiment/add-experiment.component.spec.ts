import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddExperimentComponent } from './add-experiment.component';

describe('AddExperimentComponent', () => {
  let component: AddExperimentComponent;
  let fixture: ComponentFixture<AddExperimentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddExperimentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddExperimentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
