import React, { useEffect, useState } from 'react';

// ==================================================
// GET data from server
var getUrl = 'http://localhost:5000/season-recipes'
var postUrl = 'http://localhost:5000/recipes/search'

var data = await fetch(getUrl)
  .then((response) => {
    return response.json()
  })
  .catch((err) => {
    console.log(err)
  })

// ==================================================
// UI Components

function LineBreak() {
  return <div className="line-break"></div>
}

function Ingredients(props) {
  let recipe = data.find((obj) => {
    if (obj.id == props.id) {
      return obj;
    }
  })
  return (
    <ul className="list">
      Ingredients:
      {recipe.ingredients.map((ingre) => <li key={ingre}>{ingre}</li>)}
    </ul>
  )
}

const loadRecipe = (setRecipesList, recipesList, startIndex, setStartIndex, quantity, season = 'unknown', type = 'add') => {
  
  const filter = []
  var i = startIndex
  while (true) {
    if (quantity <= 0) break
    if (season == 'unknown') {
      quantity--
      filter.push(data[i])
    } else {
      if (data[i].season == season) {
        quantity--
        filter.push(data[i])
      }
    }
    i++
  }
  setStartIndex(i)
  
  const newRecipes = filter.map(obj => (
      <div key={obj.id} className="recipe-card">
        <h1>{obj.name}</h1>
        <p style={{ opacity: 0.5, marginTop: 7 }}>Cuisine: {obj.cuisine}</p>
        <p>Season: {obj.season}</p>
        <LineBreak />
        <Ingredients id={obj.id} />
      </div>
  ))
  if (type == 'new') {
    setRecipesList(newRecipes)
  } else {
    setRecipesList([...recipesList, ...newRecipes])
  }
}

function SeasonsCheckbox({setRecipesList, setStartIndex, seasons}) {
  const [checked, setCheck] = useState()
  function checkedChange(season, setStartIndex) {
    setCheck(season)
    loadRecipe(setRecipesList, '', 0, setStartIndex, 21, season, 'new')
  }
  useEffect(() => {
    setCheck('unknown')
    loadRecipe(setRecipesList, '', 0, setStartIndex, 21, 'unknown', 'new')
  }, [])
  return (
    <div>
      {seasons.map((season) => { 
        if (season == 'unknown') {
          return (<label key={season}><input onChange = {() => checkedChange(season, setStartIndex)} 
                  checked = {checked === 'unknown'} className="season-picking" type="radio"></input>all</label>)
        } 
        return (<label key={season}><input onChange={() => checkedChange(season, setStartIndex)} 
                checked={checked === season} className="season-picking" type="radio"></input>{season}</label>)
      })}
    </div>
  )
}

function LoadMoreRecipes({ setRecipesList, recipesList, startIndex, setStartIndex }) {
  var radios = document.getElementsByClassName('season-picking')
  var season = ''
  const loadRecipes = () => {
    for (var radio of radios) {
      if (radio.checked) {
        season = radio.parentElement.textContent
        if (season == 'all') {
          season = 'unknown'
        }
        break
      }
    }
    loadRecipe(setRecipesList, recipesList, startIndex, setStartIndex, 21, season, 'add')
  }

  return (
    <React.Fragment>
      <button onClick={loadRecipes} id="loadmoreBtn">More</button>
    </React.Fragment>
  )
}

function Search() {
  
  function handleSubmit() {
    var searchValue = document.getElementById('input').value
    var ingredients = searchValue.split(' ')
      
    const post = {
        ingredients
    }
    
    fetch(postUrl,
      {
        method: "POST",
        body: JSON.stringify(post),
        headers: {
          "Content-type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((json) => console.log(json));
  }

  return (
    <div>
      <input id="input" placeholder="Nhập tên món ăn hoặc nguyên liệu" />
      <button onClick = {handleSubmit} id="searchBtn">Search</button>
    </div>
  )
}


function App() {
  const [recipes, setRecipesList] = useState([])
  const [startIndex, setStartIndex] = useState(0)
  const seasons = ['unknown', 'autumn', 'winter', 'summer', 'spring']

  return (  
    <div id="Container">
      <h1>Công thức món ăn</h1>
      <Search />
      <LineBreak />
      <SeasonsCheckbox 
        setRecipesList = {setRecipesList}
        startIndex = {startIndex}
        setStartIndex = {setStartIndex}
        seasons = {seasons}/>
      <LineBreak />
      <div id="recipe-container">
        {recipes}
        <LoadMoreRecipes
          setRecipesList = {setRecipesList}
          recipesList = {recipes}
          startIndex = {startIndex}
          setStartIndex = {setStartIndex}
        />
      </div>
    </div>
  )
}

export default App;