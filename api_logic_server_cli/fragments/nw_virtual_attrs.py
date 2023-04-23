if True:
    from safrs import jsonapi_attr
    # add derived attribute: https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py
    @jsonapi_attr
    def proper_salary(self):  # type: ignore [no-redef]
        import database.models as models
        if isinstance(self, models.Employee):
            import decimal
            rtn_value = self.Salary
            rtn_value = decimal.Decimal('1.25') * rtn_value
            self._proper_salary = int(rtn_value)
            return self._proper_salary
        else:
            print("class")
            return db.Decimal(10)

    @proper_salary.setter
    def proper_salary(self, value):  # type: ignore [no-redef]
        self._proper_salary = value
        print(f'_proper_salary={self._proper_salary}')
        pass

    ProperSalary = proper_salary  # signal safrs to recognize this as api-visible property
