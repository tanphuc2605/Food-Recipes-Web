import React, { useEffect, useState } from 'react';

// ==================================================


// ==================================================
// UI Components

function LineBreak() {
  return <div className="line-break"></div>
}

function Ingredients({ recipe }) {
  var replace = []
  if (recipe.possible_replacements) {
    replace = Object.keys(recipe.possible_replacements)
  }
  return (
    <ul className="list">
      Ingredients:
      {recipe.ingredients.map((ingre) => {
        if (recipe.possible_replacements) {
          if (recipe.possible_replacements[ingre]) {
            console.log(ingre, recipe.possible_replacements)
            return <li key={ingre}>{ingre} ({recipe.possible_replacements[ingre]})</li>
          }
          else return <li key={ingre}>{ingre}</li>
        }
        // if (replace.includes(ingre)) {
        //   for (var replacement in recipe.possible_replacements) {
        //       console.log(recipe.possible_replacements)
        //       return <li key={ingre}>{ingre} ({recipe.possible_replacements[replacement]})</li>
        //     }
        //   }
        //   else {
        //   return <li key={ingre}>{ingre}</li>
        // }
      })}
    </ul>
  )
}

const loadRecipe = (data, setRecipesList, recipesList, startIndex, setStartIndex, quantity, season = 'unknown', type = 'add') => {
  
  const filter = []
  var i = startIndex
  while (true) {
    if (quantity <= 0 || i >= data.length) break
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
        <Ingredients recipe = {obj} />
      </div>
  ))
  if (type == 'new') {
    setRecipesList(newRecipes)
  } else {
    setRecipesList([...recipesList, ...newRecipes])
  }
}

function SeasonsCheckbox({ data, setRecipesList, setStartIndex, seasons}) {
  const [checked, setCheck] = useState()
  function checkedChange(season, setStartIndex) {
    setCheck(season)
    loadRecipe(data, setRecipesList, '', 0, setStartIndex, 21, season, 'new')
  }
  useEffect(() => {
    setCheck('unknown')
    loadRecipe(data, setRecipesList, '', 0, setStartIndex, 21, 'unknown', 'new')
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

function getSeason() {
  var season = ''
  var radios = document.getElementsByClassName('season-picking')
  for (var radio of radios) {
    if (radio.checked) {
      season = radio.parentElement.textContent
      if (season == 'all') {
        season = 'unknown'
      }
      break
    }
  }
  return season
}

function LoadMoreRecipes({ data, setRecipesList, recipesList, startIndex, setStartIndex }) {
  
  var season = getSeason()
  const loadRecipes = () => {
    loadRecipe(data, setRecipesList, recipesList, startIndex, setStartIndex, 21, season, 'add')
  }

  return (
    <React.Fragment>
      <button onClick={loadRecipes} id="loadmoreBtn">More</button>
    </React.Fragment>
  )
}

function Search({ data, setData, postUrl, setRecipesList, setStartIndex }) {
  
  async function handleSubmit() {
    var searchValue = document.getElementById('input').value
    var ingredients = searchValue.split(' ')
    
    if (searchValue) {
      const post = {
          ingredients
      }
  
      var season = getSeason()
      var dataToSet = await fetch(postUrl,
        {
          method: "POST",
          body: JSON.stringify(post),
          headers: {
            "Content-type": "application/json",
          },
        })
          .then((response) => response.json())
          .catch(err => console.log(err))
      setData(dataToSet.matching)
      console.log(dataToSet)
      loadRecipe(dataToSet.matching, setRecipesList, '', 0, setStartIndex, 21, season, 'new')
    }
  }

  return (
    <div>
      <input id="input" placeholder="Nhập tên món ăn hoặc nguyên liệu" />
      <button onClick = {handleSubmit} id="searchBtn">Search</button>
    </div>
  )
}


function App() {
  const [loading, setLoading] = useState(false)
  const [recipes, setRecipesList] = useState([])
  const [data, setData] = useState([])
  const [startIndex, setStartIndex] = useState(0)
  const seasons = ['unknown', 'autumn', 'winter', 'summer', 'spring']

  // GET data from server
  var getUrl = 'http://localhost:5000/season-recipes'
  var postUrl = 'http://localhost:5000/recipes/search'

  useEffect(() => {
    async function fetchData() {
      var data = await fetch(getUrl)
      .then((response) => {
        return response.json()
      })
      .catch((err) => {
        console.log(err)
      })
      setData(data)
      setLoading(true)
    }
    fetchData()
  }, [])

  return loading ? (  
    <div id="Container">
      <h1>Công thức món ăn</h1>
      <Search 
        data = {data}
        setData = {setData}
        postUrl = {postUrl}
        setRecipesList = {setRecipesList}
        setStartIndex = {setStartIndex}
      />
      <LineBreak />
      <SeasonsCheckbox 
        data = {data}
        setRecipesList = {setRecipesList}
        setStartIndex = {setStartIndex}
        seasons = {seasons}
      />
      <LineBreak />
      <div id="recipe-container">
        {recipes}
        <LoadMoreRecipes
          data = {data}
          setRecipesList = {setRecipesList}
          recipesList = {recipes}
          startIndex = {startIndex}
          setStartIndex = {setStartIndex}
        />
      </div>
    </div>
  ) : (<div>Loading</div>)
}

export default App;