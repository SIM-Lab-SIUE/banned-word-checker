import streamlit as st
import pandas as pd
import docx
import pdfplumber
import re
from io import BytesIO

# --- NEW: EXPANDED CUSTOM CSS ---
# This block now includes color overrides for links and a custom info box style.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&family=Public+Sans:wght@400;700&display=swap');

    /* --- Font Definitions --- */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Lexend', sans-serif;
    }
    body, p, li, label, .stMarkdown {
        font-family: 'Public Sans', sans-serif;
    }
    
    /* --- Color & Style Overrides --- */

    /* Style links to use the accent color from your theme */
    a, a:visited {
        color: #ea4335 !important;
    }

    /* Create a custom info box that uses your theme's colors */
    .custom-info-box {
        background-color: #f2f2f2; /* --10-grey-color */
        border-left: 5px solid #ea4335; /* --accent-one */
        padding: 1rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


# --- BANNED WORDS SET ---
# This list remains unchanged
BANNED_WORDS = {'activism', 'activist', 'activists', 'advance diversity', 'advance inclusivity', 'advance the diversity', 'advancing diversity', 'advancing inclusive', 'advocacy', 'advocate', 'advocates', 'affirmative action', 'alliance for diversity', 'ally', 'allyship', 'antiracist', 'background inclusivity', 'barrier', 'barriers', 'bias toward', 'bias towards', 'biased', 'biased toward', 'biased towards', 'biases', 'biases toward', 'biases towards', 'bicultural', 'bipoc', 'bl cultural', 'black and latinx', 'black cultural', 'black culture', 'black cultures', 'broaden diversity', 'broaden the diversity', 'clean energy', 'climate action', 'climate change', 'climate conscious', 'climate consciousness', 'climate equality', 'climate equity', 'climate injustice', 'climate injustices', 'climate justice', 'climate justices', 'climate research', 'commitment to diversity', 'community diversity', 'community equity', 'community inclusivity', 'cultural activism', 'cultural activist', 'cultural activists', 'cultural advocacy', 'cultural advocate', 'cultural and ethnic', 'cultural and racial', 'cultural appropriation', 'cultural appropriations', 'cultural bias', 'cultural competency', 'cultural connections', 'cultural differences', 'cultural heritage', 'cultural humility', 'cultural inequalities', 'cultural inequality', 'cultural inequities', 'cultural inequity', 'cultural injustice', 'cultural injustices', 'cultural justice', 'cultural relevance', 'cultural segregation', 'culturally attuned', 'culturally biased', 'culturally responsive', 'culturally sensitive', 'culturally sustainable', 'culturally sustaining', 'culture and ethnicity', 'culture and race', 'cultures and ethnicities', 'cultures and races', 'de colonization', 'de colonize', 'de colonized', 'de colonizing', 'de segregate', 'de segregated', 'de segregates', 'de segregation', 'decolonization', 'decolonize', 'decolonized', 'decolonizing', 'dei', 'deij', 'desegregate', 'desegregated', 'desegregates', 'desegregation', 'disabilities', 'disability', 'discriminate', 'discriminated', 'discrimination', 'discriminatory', 'diverse background', 'diverse backgrounds', 'diverse communities', 'diverse community', 'diverse group', 'diverse groups', 'diverse individual', 'diverse individuals', 'diverse status', 'diverse statuses', 'diverse voices', 'diversified', 'diversify', 'diversifying', 'diversity and equity', 'diversity and inclusion', 'diversity and inclusivity', 'diversity awareness', 'diversity equity', 'divisiveness', 'eco cultural', 'ecocultural', 'ehance the diversity', 'ehancing diversity', 'emphasis on diversity', 'emphasize diversity', 'emphasizing diversity', 'encourage diversity', 'encouraging diversity', 'enhance diversity', 'enhance the diversity', 'enhancing diversity', 'environment conscious', 'environment consciousness', 'environmental conscious', 'environmental consciousness', 'environmental equality', 'environmental equity', 'environmental governance', 'environmental justice', 'environmental social', 'environmentally conscious', 'environmentalsocial', 'equal opportunities', 'equal Opportunity', 'equalities', 'equality', 'equitable', 'equitable and inclusive', 'equities', 'equity', 'esg', 'esg effort', 'esg efforts', 'esg initiative', 'esg initiatives', 'ethnic and cultural', 'ethnic cultural', 'ethnic culture', 'ethnic cultures', 'ethnic diversity', 'ethnic equity', 'ethnicities and cultures', 'ethnicity', 'ethnicity and culture', 'excluded', 'exclusion', 'exclusive', 'feel seen and heard', 'female', 'females', 'foster diversity', 'fostering diversity', 'fostering inclusive', 'fostering inclusivity', 'fostering the diversity', 'gender', 'gender diversity', 'genders', 'green infrastructure', 'green new deal', 'green society', 'group equity', 'group inclusivity', 'hate speech', 'hispanic cultural', 'hispanic culture', 'hispanic cultures', 'hispanic minority', 'hispanic people', 'hispanic person', 'hispanic voices', 'historical racism', 'historically', 'historically racist', 'historically white', 'implicit bias', 'implicit biased', 'implicit biases', 'inclusion', 'inclusive', 'inclusiveness', 'inclusivity', 'increase diversity', 'increase the diversity', 'indigenous communities', 'indigenous community', 'indigenous individual', 'indigenous individuals', 'indigenous minorities', 'indigenous minority', 'indigenous people', 'indigenous person', 'indigenous voices', 'inequalities', 'inequality', 'inequitable', 'inequities', 'injustice', 'injustices', 'institutional', 'institutional racism', 'institutional/zed racism', 'institutionalize', 'institutionalized', 'institutionally', 'institutionally racist', 'inter racial', 'inter racially', 'intergenerational trauma', 'interracial', 'interracially', 'intersectional', 'intersectionality', 'latina communities', 'latina community', 'latina individual', 'latina individuals', 'latina minorities', 'latina minority', 'latina people', 'latina person', 'latina voices', 'latinx communities', 'latinx community', 'latinx individual', 'latinx individuals', 'latinx minorities', 'latinx minority', 'latinx people', 'latinx person', 'latinx voices', 'lgbt', 'marginalization', 'marginalize', 'marginalized', 'micro aggression', 'micro aggressions', 'micro aggressive', 'micro aggressiveness', 'microaggression', 'microaggressions', 'microaggressive', 'microaggressiveness', 'minorities', 'minority', 'multi ethnic', 'multi ethnically', 'multicultural', 'multiethnic', 'multiethnically', 'net zero', 'netzero', 'non black', 'non white', 'nonblack', 'nonwhite', 'oppressed', 'oppression', 'oppressive', 'oppressiveness', 'people of color', 'poc', 'pocx', 'polarization', 'polarize', 'political', 'politicization', 'politicize', 'predominately white', 'prejudice', 'prejudices', 'primarily white', 'priviledges', 'privilege', 'privileged', 'privileged white', 'privileges', 'pro black', 'pro white', 'prob lack', 'promoting diversity', 'race and culture', 'race and ethnicity', 'race based', 'racebased', 'races and cultures', 'races and ethnicities', 'racial', 'racial and cultural', 'racial and ethnic', 'racial bias', 'racial biases', 'racial disparities', 'racial disparity', 'racial diversity', 'racial identity', 'racial inequalities', 'racial inequality', 'racial inequities', 'racial inequity', 'racial injustice', 'racial injustices', 'racial justice', 'racial minorities', 'racial minority', 'racial oppression', 'racial prejudice', 'racial prejudices', 'racial segregation', 'racial socialization', 'racial solidarity', 'racial stereotypes', 'racial violence', 'racially', 'racially and culturally', 'racially bias', 'racially biased', 'racially oppressed', 'racism', 'racist', 'reparation', 'reparations', 'safe space', 'safe spaces', 'segregated', 'segregated ethnicities', 'segregated ethnicity', 'segregated race', 'segregated races', 'segregation', 'sense of belonging', 'sense of belongingness', 'sexual preferences', 'social environmental', 'social justice', 'socialenvironmental', 'socio cultural', 'socio economic', 'sociocultural', 'socioeconomic', 'status', 'statuses', 'stereotype', 'stereotypes', 'stereotypical', 'stereotyping', 'structural racism', 'structurally racist', 'system of oppression', 'systematic oppression', 'systematically oppressed', 'systemic', 'systemic oppression', 'systemic racism', 'systemical', 'systemically', 'systemically oppressed', 'systemically racist', 'systems of oppression', 'systems of power', 'tokenistic', 'tokensim', 'trans ethnic', 'transethnic', 'trauma', 'traumatic', 'under appreciated', 'under appreciation', 'under privilege', 'under privileged', 'under representation', 'under represented', 'under served', 'under serving', 'under valued', 'under valuing', 'underappreciated', 'underappreciation', 'underprivilege', 'underprivileged', 'underrepresentation', 'underrepresented', 'underserved', 'underserving', 'undervalued', 'undervaluing', 'unequal opportunities', 'unequal opportunity', 'unjust', 'victim', 'victimhood', 'victimized', 'victims', 'voices are acknowledged', 'voices heard', 'voices matter', 'welcoming environment', 'white colonialism', 'white colonization', 'white colonizer', 'white colonizers', 'white fragility', 'white historically', 'white nationalism', 'white nationalist', 'white people', 'white person', 'white privilege', 'white serving', 'white supremacy', 'whiteness', 'women', 'women and underrepresented'}


# --- TEXT EXTRACTION FUNCTIONS ---
def extract_text_from_docx(file_like_object):
    try:
        doc = docx.Document(file_like_object)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"Error reading .docx file: {e}")
        return ""

def extract_text_from_pdf(file_like_object):
    text = ""
    try:
        with pdfplumber.open(file_like_object) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading .pdf file: {e}")
        return ""

# --- STREAMLIT APP UI ---
st.set_page_config(
    page_title="SIM Lab Word Checker",
    page_icon="🔬",
    layout="wide"
)

# --- SIDEBAR FOR BRANDING ---
with st.sidebar:
    st.image("assets/simlab-atsiue.png")
    st.image("assets/siue-red-logo.png")
    st.markdown("---")
    st.markdown(
        "This tool is provided by the **SIM Lab** at "
        "**Southern Illinois University Edwardsville**."
    )
    st.markdown("[Visit the SIM Lab Website](https://www.siue.edu/education/secondary-education/simlab/)")
    st.markdown("[Visit SIUE's Website](https://www.siue.edu)")
    st.markdown("---")


# --- Main page content ---
st.title("Banned Words Checker for Federal Grants")

# --- REPLACED st.info() WITH CUSTOM st.markdown() ---
st.markdown('<div class="custom-info-box">Upload a .docx or .pdf document to check for the presence and frequency of specific words and phrases.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop your file here or click to upload",
    type=['docx', 'pdf'],
    accept_multiple_files=False
)

if uploaded_file is not None:
    file_bytes = BytesIO(uploaded_file.getvalue())
    
    if uploaded_file.name.endswith('.pdf'):
        raw_text = extract_text_from_pdf(file_bytes)
    elif uploaded_file.name.endswith('.docx'):
        raw_text = extract_text_from_docx(file_bytes)
    else:
        raw_text = ""
        st.error("Unsupported file format.")

    if raw_text:
        st.subheader("Analysis Results")
        
        normalized_text = raw_text.lower()
        
        found_words = {}
        for phrase in BANNED_WORDS:
            try:
                pattern = r'\b' + re.escape(phrase) + r'\b'
                matches = re.findall(pattern, normalized_text)
                if matches:
                    found_words[phrase] = len(matches)
            except re.error as e:
                st.warning(f"Could not process phrase '{phrase}': {e}")
                continue

        if found_words:
            df = pd.DataFrame(list(found_words.items()), columns=['Banned Phrase', 'Frequency'])
            df = df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.success("🎉 **Great news!** No banned words were found in your document.")