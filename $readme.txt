app
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
        SSQLALCHEMY_DATABASE_URI = "sqlite:////Users/val/dev/ApiLogicServer/app_logic_server/nw.sqlite"

view.py
    x ProductDetails_V

sakila
    table cycle Store -> Staff
    bad field name film.release_year



class StoreModelView(ModelView):
   datamodel = SQLAInterface(Store)
   list_columns = ["store_id", "staff.first_name", "addres.address_id", "last_update"]
   show_columns = ["store_id", "staff.first_name", "addres.address_id", "last_update", "manager_staff_id", "address_id"]
   edit_columns = ["store_id", "last_update", "manager_staff_id", "address_id"]
   add_columns = ["store_id", "last_update", "manager_staff_id", "address_id"]
   related_views = [   --> StaffModelView, InventoryModelView, CustomerModelView]

appbuilder.add_view(
      StoreModelView, "Store List", icon="fa-folder-open-o", category="Menu")


# table already generated per recursion: rental
# table already generated per recursion: payment



class StaffModelView(ModelView):
   datamodel = SQLAInterface(Staff)
   list_columns = ["first_name", "store.store_id", "addres.address_id", "last_name", "picture"]
   show_columns = ["first_name", "store.store_id", "addres.address_id", "last_name", "picture", "email", "active", "username", "password", "last_update", "store_id", "address_id", "staff_id"]
   edit_columns = ["first_name", "last_name", "picture", "email", "active", "username", "password", "last_update", "store_id", "address_id", "staff_id"]
   add_columns = ["first_name", "last_name", "picture", "email", "active", "username", "password", "last_update", "store_id", "address_id", "staff_id"]
   related_views = [ ---> StoreModelView, RentalModelView, PaymentModelView]
