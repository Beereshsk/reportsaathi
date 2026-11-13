const fileInput=document.getElementById('fileInput');
const panel=document.getElementById('inputPanel');
const textarea=document.getElementById('prescriptionText');
const imageEntry=document.getElementById('imageEntry');
const textEntry=document.getElementById('textEntry');
const toast=document.getElementById('toast');
let imageUrl=null;
let toastTimer;
let lastSummary = "";
const apiBaseUrl=window.__API_URL__||(window.location.hostname==='localhost'||window.location.hostname==='127.0.0.1'?`${window.location.protocol}//${window.location.hostname}:5000/api`:'/api');
function showToast(message){toast.textContent=message;toast.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.classList.remove('show'),2600)}
function openPanel(mode){panel.hidden=false;document.getElementById('results').hidden=true;imageEntry.hidden=mode!=='image';textEntry.hidden=mode==='image';document.getElementById('panelTitle').textContent=mode==='image'?'Your image is ready to view':'Type the instructions you can read';document.getElementById('panelHint').textContent=mode==='image'?'Check your image, then type any details you can read. This prototype does not extract text from images.':'Copy the medicine name and directions as written. Leave anything you’re unsure about blank.';panel.scrollIntoView({behavior:'smooth',block:'center'})}
document.getElementById('cameraButton').addEventListener('click',()=>{fileInput.setAttribute('capture','environment');fileInput.click()});
document.getElementById('uploadButton').addEventListener('click',()=>{fileInput.removeAttribute('capture');fileInput.click()});
document.getElementById('typeButton').addEventListener('click',()=>{openPanel('text');setTimeout(()=>textarea.focus(),250)});
fileInput.addEventListener('change',()=>{const file=fileInput.files&&fileInput.files[0];if(!file)return;const allowedTypes=['image/jpeg','image/png','image/webp'];if(!allowedTypes.includes(file.type)){showToast('Choose a JPEG, PNG, or WebP image.');fileInput.value='';return}if(file.size>10*1024*1024){showToast('Choose an image smaller than 10 MB.');fileInput.value='';return}if(imageUrl)URL.revokeObjectURL(imageUrl);imageUrl=URL.createObjectURL(file);document.getElementById('previewImage').src=imageUrl;document.getElementById('fileName').textContent=file.name;openPanel('image')});
document.getElementById('removeImage').addEventListener('click',()=>{if(imageUrl)URL.revokeObjectURL(imageUrl);imageUrl=null;fileInput.value='';openPanel('text')});
document.getElementById('closePanel').addEventListener('click',()=>{panel.hidden=true});
document.getElementById('imageContinue').addEventListener('click',()=>{openPanel('text');textarea.focus()});
async function renderMedicineResults(data) {
  const output = document.getElementById('notesOutput');
  output.replaceChildren();
  const summaries = [];

  for (const medicine of data.medicines) {
    const card = document.createElement('article');
    card.className = medicine.is_ambiguous ? 'medicine-result medicine-result-unclear' : 'medicine-result';
    const title = document.createElement('h4');
    title.textContent = medicine.raw_name;
    card.append(title);

    const dose = document.createElement('p');
    dose.textContent = `Dose/strength as written: ${medicine.dosage}`;
    card.append(dose);

    const timing = medicine.timing;
    const timeText = timing.morning + timing.afternoon + timing.night > 0
      ? `Morning: ${timing.morning}, afternoon: ${timing.afternoon}, night: ${timing.night}`
      : 'Timing: unclear';
    const timingLine = document.createElement('p');
    timingLine.textContent = timeText;
    card.append(timingLine);

    const mealLabels = { before_food: 'Before food', after_food: 'After food', with_food: 'With food', unspecified: 'Food timing: not specified' };
    const mealLine = document.createElement('p');
    mealLine.textContent = mealLabels[medicine.meal_relation] || 'Food timing: unclear';
    card.append(mealLine);

    if (medicine.duration_days !== null && medicine.duration_days !== undefined) {
      const durationLine = document.createElement('p');
      durationLine.textContent = `Duration as written: ${medicine.duration_days} days`;
      card.append(durationLine);
    }

    if (medicine.is_ambiguous) {
      const warning = document.createElement('p');
      warning.className = 'medicine-warning';
      warning.textContent = medicine.ambiguity_reason || 'Some details are unclear. Confirm with your pharmacist.';
      card.append(warning);
    }

    output.append(card);
    summaries.push([title.textContent, dose.textContent, timeText, mealLine.textContent,
      medicine.duration_days ? `Duration: ${medicine.duration_days} days` : '',
      medicine.ambiguity_reason || ''].filter(Boolean).join('. '));
  }
  lastSummary = summaries.join('\n\n');
}

async function showNotes() {
  const notes = textarea.value.trim();
  if (!notes) {
    showToast('Type the instructions you can read first.');
    textarea.focus();
    return;
  }

  const button = document.getElementById('reviewButton');
  button.disabled = true;
  button.setAttribute('aria-busy', 'true');
  try {
    const response = await fetch(`${apiBaseUrl}/extract`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ raw_text: notes, language: document.documentElement.lang === 'kn' ? 'kn' : 'en' }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'The server could not read these instructions.');

    renderMedicineResults(data);
    panel.hidden = true;
    const results = document.getElementById('results');
    results.hidden = false;
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (error) {
    showToast(error instanceof Error ? error.message : 'Could not connect to the prescription service. Please try again.');
  } finally {
    button.disabled = false;
    button.removeAttribute('aria-busy');
  }
}
document.getElementById('reviewButton').addEventListener('click',()=>{void showNotes()});
document.getElementById('startOver').addEventListener('click',()=>{textarea.value='';lastSummary='';panel.hidden=true;document.getElementById('results').hidden=true;if(imageUrl)URL.revokeObjectURL(imageUrl);imageUrl=null;fileInput.value='';window.scrollTo({top:0,behavior:'smooth'})});
document.getElementById('speakButton').addEventListener('click',()=>{if(!('speechSynthesis'in window)){showToast('Read aloud is not supported in this browser.');return}window.speechSynthesis.cancel();const utterance=new SpeechSynthesisUtterance(lastSummary);utterance.lang=document.documentElement.lang==='kn'?'kn-IN':'en-IN';window.speechSynthesis.speak(utterance)});
document.getElementById('shareButton').addEventListener('click',async()=>{const message='My prescription notes (please verify these with a doctor or pharmacist):\n\n'+lastSummary+'\n\nPlease confirm all medicine details with your doctor or pharmacist before taking any medicine.';if(navigator.share){try{await navigator.share({text:message})}catch(error){if(error.name!=='AbortError')showToast('Could not open the share menu.')}}else{window.open('https://wa.me/?text='+encodeURIComponent(message),'_blank','noopener');}});
document.getElementById('fontButton').addEventListener('click',event=>{document.body.classList.toggle('large-text');event.currentTarget.innerHTML=document.body.classList.contains('large-text')?'<span>Aa</span> Standard text':'<span>Aa</span> Larger text'});
const englishText=new Map();
const kannadaText={'.brand span:last-child':'ಔಷಧ ಸಾಥಿ','main .eyebrow':'ಸ್ವಲ್ಪ ಸ್ಪಷ್ಟತೆ, ಹೆಚ್ಚಿನ ನೆಮ್ಮದಿ','.hero h1':'ಔಷಧದ ಸೂಚನೆಗಳು,\nಇನ್ನಷ್ಟು ಸರಳವಾಗಿ.','.hero-copy>p':'ನಿಮ್ಮ ವೈದ್ಯರು ಬರೆದದ್ದನ್ನು ಒಂದೊಂದಾಗಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ. ಫೋಟೋ ತೆಗೆಯಿರಿ, ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಇಲ್ಲಿ ಬರೆಯಿರಿ.','.trust-line':'✳ ನಿಮ್ಮ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಹಾಯ — ರೋಗನಿರ್ಣಯವಲ್ಲ.','.section-heading h2':'ಹೇಗೆ ಪ್ರಾರಂಭಿಸಲು ಬಯಸುತ್ತೀರಿ?','#cameraButton .card-copy b':'ಫೋಟೋ ತೆಗೆಯಿರಿ','#cameraButton .card-copy small':'ಕ್ಯಾಮೆರಾದಿಂದ ಚಿತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ','#uploadButton .card-copy b':'ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ','#uploadButton .card-copy small':'ಫೋಟೋ ಅಥವಾ ಸ್ಕ್ಯಾನ್ ಆಯ್ಕೆಮಾಡಿ','#typeButton .card-copy b':'ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ','#typeButton .card-copy small':'ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ನಲ್ಲಿರುವುದನ್ನು ಬರೆಯಿರಿ','.how-heading h2':'ನಿಮಗೆ ಬೇಕಾದಾಗ ಸ್ವಲ್ಪ ಸಹಾಯ.','.notes-title b':'ನಿಮ್ಮ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಟಿಪ್ಪಣಿಗಳು','.notes-foot':'ಸ್ಪಷ್ಟವಿಲ್ಲದ ವಿವರಗಳನ್ನು ಔಷಧಿಕಾರರೊಂದಿಗೆ ಪರಿಶೀಲಿಸಿ.','footer>span:nth-child(2)':'ನಿಮಗೆ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಸಹಾಯ — ನಿಮ್ಮ ವೈದ್ಯರ ಆರೈಕೆಗೆ ಬದಲಿ ಅಲ್ಲ.','#safety':'✳ ಯಾವುದೇ ಔಷಧ ತೆಗೆದುಕೊಳ್ಳುವ ಮೊದಲು ವಿವರಗಳನ್ನು ನಿಮ್ಮ ವೈದ್ಯರು ಅಥವಾ ಔಷಧಿಕಾರರೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.'};
function setLanguage(kannada){document.documentElement.lang=kannada?'kn':'en';for(const selector of Object.keys(kannadaText)){const el=document.querySelector(selector);if(!el)continue;if(!englishText.has(selector))englishText.set(selector,el.textContent);el.textContent=kannada?kannadaText[selector]:englishText.get(selector)}document.getElementById('languageToggle').innerHTML=kannada?'ಕನ್ನಡ <span class="lang-separator">/</span> <b>EN</b>':'ಕನ್ನಡ <span class="lang-separator">/</span> <b>EN</b>';document.getElementById('languageToggle').setAttribute('aria-label',kannada?'ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗಿದೆ; ಇಂಗ್ಲಿಷ್‌ಗಾಗಿ ಒತ್ತಿರಿ':'Switch language');}
document.getElementById('languageToggle').addEventListener('click',()=>setLanguage(document.documentElement.lang!=='kn'));
window.addEventListener('pagehide',()=>{if(imageUrl)URL.revokeObjectURL(imageUrl);if('speechSynthesis'in window)window.speechSynthesis.cancel()});
