function openModal(id){document.getElementById(id).style.display="grid"}
function closeModal(id){document.getElementById(id).style.display="none"}
function switchModal(){
  const login=document.getElementById("loginModal");
  const register=document.getElementById("registerModal");
  const loginOpen=login.style.display==="grid";
  login.style.display=loginOpen?"none":"grid";
  register.style.display=loginOpen?"grid":"none";
}
window.onclick=e=>{
  if(e.target.classList.contains("modal")) e.target.style.display="none";
}

async function findPlaces(){
  const box=document.getElementById("matches");
  box.innerHTML="<div class='match'><p>Calculating transparent match scores...</p></div>";
  const response=await fetch("/api/recommend",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      budget:Number(document.getElementById("pBudget").value),
      days:Number(document.getElementById("pDays").value),
      interest:document.getElementById("pInterest").value,
      low_crowd:document.getElementById("pCrowd").checked
    })
  });
  const data=await response.json();

  box.innerHTML=data.map(d=>`
    <article class="match">
      <div class="score">${d.match}</div>
      <small>/ 100 match</small>
      <h3>${d.emoji} ${d.name}</h3>
      <p>${d.state} · ${d.crowd} crowd · ${d.eco}/100 impact</p>
      <p style="margin-top:8px">Approx. ₹${d.budget.toLocaleString("en-IN")} · ${d.days} days</p>
      <div class="match-actions">
        <button class="small-btn" onclick="buildItinerary('${d.name}',${d.days},${d.budget})">Build itinerary</button>
      </div>
    </article>
  `).join("");
}

async function buildItinerary(destination,days,budget){
  const response=await fetch("/api/itinerary",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({destination,days})
  });
  const data=await response.json();
  const text=data.map(d=>`${d.title}\n• ${d.activities.join("\n• ")}`).join("\n\n");

  const save=confirm(
    text +
    "\n\nPress OK to save this trip to your dashboard, or Cancel to keep it as a preview."
  );

  if(save){
    const r=await fetch("/api/save-trip",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({destination,days,budget,itinerary:text})
    });
    if(r.status===401){
      alert("Please login first, then build the itinerary again.");
    }else{
      const result=await r.json();
      if(result.success) alert("Trip saved. Open My Trips from the navigation.");
    }
  }
}
