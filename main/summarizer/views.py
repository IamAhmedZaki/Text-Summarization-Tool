# summarizer/views.py
from django.shortcuts import render
from .forms import SummaryForm
import nltk
import spacy
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load resources once
nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
t5_tokenizer = T5Tokenizer.from_pretrained("t5-small")
t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

def extractive_summary(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return ' '.join(sentences[:3])  # Top 3 sentences for demo

def abstractive_summary(text):
    input_text = "summarize: " + text
    input_ids = t5_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = t5_model.generate(input_ids, max_length=150, min_length=40, num_beams=4, early_stopping=True)
    return t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_view(request):
    summary = ""
    if request.method == 'POST':
        form = SummaryForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            method = form.cleaned_data['method']
            if method == 'extractive':
                summary = extractive_summary(text)
            else:
                summary = abstractive_summary(text)
    else:
        form = SummaryForm()
    return render(request, 'summarizer.html', {'form': form, 'summary': summary})
