def get_prompt(client, A):
	prompt = f"""
	Generate a realistic dialogue between a client experiencing an acute panic attack and an online Psychological First Aid (PFA) counselor over a call.  
	The dialogue must be based on the **dialogue history** and the **counselor's plan** for Step A (LOOK Phase) of the PFA Handbook.

	---

	##  Step A (LOOK Phase) in PFA

	Psychological First Aid (PFA) is a structured approach used to support people in crisis.  
	The **LOOK Phase (Step A)** is the first step, where the counselor:
	- Assesses the client's **physical symptoms**, **emotional state**, and **catastrophic thinking**
	- Ensures the client is in a **safe and quiet environment**

	The counselor’s goal is to gather all four pieces of required information:

	- **[A.Q1] Physical Symptoms**  
	- **[A.Q2] Emotional State**  
	- **[A.Q3] Catastrophic Thinking**  
	- **[A.P1] Ensure Safety**

	---

	## 🧾 Client Profile (not visible to the counselor)
	- Environment: {{client['environment']}}  
	- Physical Symptoms: {{client['physical_symptom']}}  
	- Emotion: {{client['emotional_react']}}  
	- Thought: "{{client['catastrophic_thought']}}"  
	- Trigger: {{client['trigger']}}  

	---

	---

	## Client Behavior
	- The client may initially struggle to follow instructions.
	- As stabilization progresses, their responses may become clearer and calmer.
	- If severity is high, simulate fragmented or gasping speech.
	---

	## ✅ Output Format (One Turn Only)

	Each dialogue turn must include the following fields:

	- `"counselor"`: The counselor’s spoken utterance  
	- `"client"`: The client's response  
	- `"possible_to_end_reasoning"`:  
	A reasoning string that answers:
	1. Have all four required elements (symptoms, emotion, thought, safety) been covered?
	2. If yes, end with `"MOVE"`  
	3. If not, end with `"KEEP"`

	- If the `possible_to_end_reasoning` ends with `"MOVE"`, **do not include or generate a counselor utterance** — the session ends.  

	Format:
	```json
	{{
	"counselor": "<counselor's utterance>",
	"client": "<client's response>",
	"possible_to_end_reasoning": "The client's physical symptoms, emotional state, and catastrophic thinking have been identified, but their safety has not yet been fully confirmed. Therefore, my decision is KEEP"
	}}
	```
	"""
	return prompt
