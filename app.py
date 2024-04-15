from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Milagros@localhost/pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


with app.app_context():
   connect_db(app)
   db.drop_all()
   db.create_all()

# Create some dummy data for pets
dummy_data = [
    {
        "name": "Buddy",
        "species": "Dog",
        "photo_url": "./static/baby1.jpeg",
        "age": 3,
        "notes": "Friendly and playful",
        "available": True,
    },
    {
        "name": "Whiskers",
        "species": "Cat",
        "photo_url": "./static/baby2.jpeg",
        "age": 2,
        "notes": "Loves to nap",
        "available": False,
    },
    {
        "name": "Rocky",
        "species": "Hamster",
        "photo_url": None,
        "age": 1,
        "notes": "Small and cute",
        "available": True,
    },
]

with app.app_context():
    for pet_data in dummy_data:
        new_pet = Pet(**pet_data)
        db.session.add(new_pet)
    db.session.commit()

@app.route('/')
def show_home_page():
    pets = Pet.query.all()
    return render_template('base.html', pets = pets)

@app.route('/add', methods= ['GET', 'POST'])
def add_pet_form():
    """Pet add form; handle adding."""
    form = AddPetForm()
    
    if form.validate_on_submit():
        new_pet = Pet (
            name = form.name.data,
            age = form.age.data,
            species = form.species.data,
            photo_url = form.photo_url.data,
            notes = form.notes.data,
            available = form.available.data
        )

        db.session.add(new_pet)
        db.session.commit()
       
        flash(f'Added {new_pet.name} to Pets list.')
        return redirect('/')
    
    else:
        return render_template('/addPetForm.html', form = form)
    

@app.route("/<int:petId>/edit", methods =['POST', 'GET'])
def edit_pet_form(petId):
    """Show pet edit form and handle edit."""
    pet = Pet.query.get_or_404(petId)
    form = AddPetForm(obj=pet)

    if request.method == 'POST' and form.validate():
         pet.photo_url = form.photo_url.data
         pet.notes = form.notes.data
         pet.available = form.available.data
         db.session.commit()
         flash(f"Pet {pet.name} updated!")
         return redirect(f"/{petId}/edit")
    
    return render_template("editPet.html", pet=pet, form=form)


