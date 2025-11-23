## Step 3 – Retrieval & Answer Evaluation

- **Model used for /query**: models/gemini-2.5-pro
- **Number of evaluated questions**: 20
- **Answer accuracy**: 70.0%
- **Page-reference accuracy**: 18.0%

### Q1

- **Question**: I'm calculating our takeoff weight for a dry runway. We're at 2,000 feet pressure altitude, and the OAT is 50°C. What's the climb limit weight ?
- **Labelled answer**: Based on the data for a dry runway at 2,000 feet pressure altitude with an OAT of 50°C, the Climb Limit Weight is 52,200 kg.
- **Model answer**: Based on the "Takeoff Field & Climb Limit Weights - Dry Runway" table for **2000 FT Pressure Altitude**, the climb limit weight at an OAT of **50°C** is **52.2 (1000 KG)**.
- **Labelled pages**: 83
- **Returned pages**: 26, 83, 104, 106, 107
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q2

- **Question**: We're doing a Flaps 15 takeoff. Remind me, what is the first flap selection we make during retraction, and at what speed?
- **Labelled answer**: For a Flaps 15 takeoff, the first flap selection during retraction is Flaps 5, which you select at V2 + 15 knots.
- **Model answer**: Based on the "Takeoff Flap Retraction Speed Schedule" table on page 41, for a Flaps 15 takeoff, the first flap selection is **Flaps 5** at a speed of **V2 + 15**.
- **Labelled pages**: 41
- **Returned pages**: 40, 41, 53, 54, 55
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q3

- **Question**: We're planning a Flaps 40 landing on a wet runway at a 1,000-foot pressure altitude airport. If the wind-corrected field length is 1,600 meters, what is our field limit weight?
- **Labelled answer**: For a Flaps 40 landing on a wet runway at 1,000 feet pressure altitude with a 1,600-meter wind-corrected field length, the field limit weight is 55,800 kg
- **Model answer**: Based on the "Field Limit Weight (1000 KG)" table for a Flaps 40 landing:

1.  **Locate the Airport Pressure Altitude:** Find the main column for **1000** FT.
2.  **Select Runway Condition:** Within the 1000 FT column, find the sub-column for a **WET** runway.
3.  **Find the Field Length:** Go down the "WIND CORR'D FIELD LENGTH (M)" column to the row for **1600**.
4.  **Read the Value:** The value at the intersection of the 1600 M row and the 1000 FT / WET column is **55.8**.

Since the weight is given in 1000 KG, the field limit weight is **55,800 kg**.
- **Labelled pages**: 99
- **Returned pages**: 82, 83, 85, 86, 99
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q4

- **Question**: Reviewing the standard takeoff profile: After we're airborne and get a positive rate of climb, what is the first action we take?
- **Labelled answer**: After getting a positive rate of climb, the first action is to call for "GEAR UP". This is shown in both the "Takeoff Procedure" table and the "Takeoff" flight pattern diagram.
- **Model answer**: Based on the "Go-around" and "Missed approach" procedures shown in the visual diagrams, the first action after establishing a positive rate of climb is to raise the landing gear.

Looking at the **Visual Traffic Pattern** diagram (Page 56), in the "Go-around" section, the fifth bullet point states:
- **Positive rate of climb gear up**
- **Labelled pages**: 39, 51
- **Returned pages**: 40, 46, 53, 54, 56
- **Answer correctness (YES/NO)**: NO
- **Page reference correctness (0–10)**: 0.00
### Q5

- **Question**: Looking at the panel scan responsibilities for when the aircraft is stationary, who is responsible for the forward aisle stand?
- **Labelled answer**: Based on the "Panel Scan Diagram" for when the airplane is not moving under its own power, the Captain is responsible for the forward aisle stand (the area labeled with the number 6).
- **Model answer**: Based on the "Panel Scan Diagram" on page 6, the responsibility for the forward aisle stand is split.

*   **The Captain** is responsible for the left side of the forward aisle stand (the area with the white background).
*   **The First Officer** is responsible for the right side of the forward aisle stand (the area with the gray background).
- **Labelled pages**: 6
- **Returned pages**: 4, 6, 109, 131, 133
- **Answer correctness (YES/NO)**: NO
- **Page reference correctness (0–10)**: 2.00
### Q6

- **Question**: For a standard visual pattern, what three actions must be completed prior to turning base?
- **Labelled answer**: According to the "Visual Traffic Pattern" diagram, the three actions to complete prior to turning base are:
Gear down
Flaps 15 (landing flaps for 1 engine)
Arm speedbrake
- **Model answer**: Based on the "Visual Traffic Pattern" diagram on page 56, the three actions that must be completed prior to turning base are:

1.  **Gear down**
2.  **Flaps 15 (landing flaps for 1 engine)**
3.  **Arm speedbrake**
- **Labelled pages**: 56
- **Returned pages**: 4, 5, 42, 56, 67
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q7

- **Question**: When the Pilot Not Flying (PNF) makes CDU entries during flight, what must the Pilot Flying (PF) do prior to execution
- **Labelled answer**: The Pilot Flying must verify the entries prior to execution.
- **Model answer**: Based on the "CDU Operation" section on Page 5 of the manual, when the Pilot Not Flying (PNF) makes CDU entries during flight, the Pilot Flying (PF) must **verify** the entries prior to execution.

This is stated in the text: "In flight, CDU entries are normally accomplished by the pilot not flying and **verified by the pilot flying prior to execution**."
- **Labelled pages**: 5
- **Returned pages**: 4, 5, 7, 29, 67
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q8

- **Question**: I see an amber "STAIRS OPER" light illuminated on the forward attendant panel; what does that light indicate?
- **Labelled answer**: That amber STAIRS OPER (Operating) light indicates that the airstair is in transit (i.e., currently extending or retracting).
- **Model answer**: Based on the "Forward Airstairs" section on page 126 of the manual, the amber "STAIRS OPER" light indicates the following:

**The airstair is in transit.**
- **Labelled pages**: 126
- **Returned pages**: 11, 114, 115, 126, 131
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q9

- **Question**: We've just completed the engine start. What is the correct configuration for the ISOLATION VALVE switch during the After Start Procedure?
- **Labelled answer**: During the After Start Procedure, the ISOLATION VALVE switch should be set to AUTO.
- **Model answer**: According to the After Start Procedure on Page 35, the correct configuration for the ISOLATION VALVE switch is **AUTO**.
- **Labelled pages**: 35
- **Returned pages**: 33, 34, 35, 64, 65
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q10

- **Question**: During the Descent and Approach procedure, what action is taken with the AUTO BRAKE select switch , and what is the Pilot Flying's final action regarding the autobrake system during the Landing Roll procedure?
- **Labelled answer**: Here are the autobrake actions for those two phases of flight:
Descent and Approach Procedure
During the Descent and Approach Procedure, you set the AUTO BRAKE select switch to the desired brake setting.

Landing Roll Procedure
The Pilot Flying's final action regarding the autobrake system is to disarm the autobrake prior to reaching taxi speed.
- **Model answer**: Based on the Boeing 737 Operations Manual excerpts provided:

*   **Descent and Approach Procedure:** The provided text, specifically the "Approach Procedure" on page 44, does not contain instructions regarding the AUTO BRAKE select switch.

*   **Landing Roll Procedure:** According to the "Landing Roll Procedure" table on page 47, under the **PILOT FLYING** column, the final action regarding the autobrake system is: **"Prior to taxi speed, disarm the autobrake and continue manual braking as required."**
- **Labelled pages**: 43, 47
- **Returned pages**: 4, 40, 44, 47, 67
- **Answer correctness (YES/NO)**: NO
- **Page reference correctness (0–10)**: 2.00
### Q11

- **Question**: We need to hold at 10,000 feet, and our weight is 60,000 kg. What is the expected total fuel flow in kilograms per hour?
- **Labelled answer**: The expected total fuel flow for holding at 10,000 feet with a weight of 60,000 kg is 2100 kilograms per hour (KG/HR). It is important to note that the fuel flow value provided in this table already includes a 5% additional fuel allowance for holding in a racetrack pattern
- **Model answer**: Based on the documents provided, I cannot answer your question.

The section titled "Holding Planning" on Page 105 describes the exact table needed to answer your question, but the table itself is not included in the provided pages.
- **Labelled pages**: 93
- **Returned pages**: 88, 102, 105, 106, 144
- **Answer correctness (YES/NO)**: NO
- **Page reference correctness (0–10)**: 0.00
### Q12

- **Question**: I'm looking at the exterior light switches on the overhead panel. What is the function of the TAXI Light switch?
- **Labelled answer**: The TAXI Light switch controls the taxi light, which is mounted on the nose wheel strut.

OFF: The nose wheel well taxi light is extinguished.

ON: The nose wheel well taxi light is illuminated.
- **Model answer**: Based on the "Exterior Lighting" diagram on page 112, the function of the TAXI Light switch is as follows:

*   **OFF** – nose wheel well taxi light extinguished.
*   **ON** – nose wheel well taxi light illuminated.
- **Labelled pages**: 112, 131
- **Returned pages**: 32, 109, 112, 131, 134
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 4.00
### Q13

- **Question**: where exactly are the Logo Lights located on the airframe?
- **Labelled answer**: Based on the manual, the Logo Lights are located on the top of each horizontal stabilizer surface.

They are positioned to point light onto both sides of the vertical stabilizer.
- **Model answer**: Based on the provided documents, the Logo Lights are located **on the top of each horizontal stabilizer surface**.

This is stated in the text on page 131:
"Logo lights are located on the top of each horizontal stabilizer surface to point light on both sides of the vertical stabilizer."

This location is also confirmed by the diagram on page 133, which shows labels for "LOGO LIGHT (white)" pointing to each of the horizontal stabilizers at the tail of the aircraft.
- **Labelled pages**: 131
- **Returned pages**: 113, 131, 133, 134, 139
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q14

- **Question**: I'm preparing for a Flaps 15 go-around. If our weight-adjusted gradient is 4% and our speed is VREF+20, what is the gradient adjustment for speed?
- **Labelled answer**: Based on the "ENGINE INOP Go-Around Climb Gradient Flaps 15" table, the gradient adjustment for speed when flying at VREF+20 with a weight-adjusted go-around gradient of 4% is 0.28%
- **Model answer**: Based on the "Gradient Adjustment for Speed (%)" table on Page 101, the correct value is **0.28**.

Here is how to find it:
1.  Locate the **Gradient Adjustment for Speed (%)** table.
2.  Find the row corresponding to the speed **VREF+20**.
3.  Find the column corresponding to the weight adjusted go-around gradient of **4**.
4.  The value at the intersection of this row and column is **0.28**.
- **Labelled pages**: 101
- **Returned pages**: 40, 44, 101, 105, 107
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q15

- **Question**: I'm holding the BCF (Halon) fire extinguisher. After I pull the ring pin, what is the action required to discharge the agent?
- **Labelled answer**: After pulling the ring pin, you must press the top lever to discharge the agent.

The manual also recommends aiming at the base of the fire from a distance of six feet.
- **Model answer**: Based on the "To use the Halon fire extinguisher" section on page 146, the action required to discharge the agent after pulling the ring pin is:

**press top lever**

The full instruction is: "aim at base of fire from a distance of six feet and press top lever".
- **Labelled pages**: 146
- **Returned pages**: 11, 23, 137, 145, 146
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q16

- **Question**: I'm calculating my takeoff performance. The available runway is 2,000 meters with a 1.0% uphill slope. Factoring in a 10-knot tailwind, what is the final slope and wind-corrected field length I should use?
- **Labelled answer**: Here is the two-step calculation based on the "Takeoff Field Corrections - Dry Runway" tables:

Step 1: Slope Correction

Using the "Slope Corrections" table, find the row for FIELD LENGTH AVAILABLE (M) of 2000.

Find the column for RUNWAY SLOPE (%) of 1.0 (uphill).

The intersection gives a Slope Corrected Field Length of 1,760 meters.

Step 2: Wind Correction

Using the "Wind Corrections" table, you must use the 1,760-meter value from Step 1 as your input. This requires interpolation between the 1600m and 1800m rows.

Find the column for a 10-knot tailwind (the "10" column).

The value for a 1600m corrected length is 1680.

The value for a 1800m corrected length is 1880.

Interpolating for your 1,760m length gives a final value of 1,840 meters.

The final slope and wind-corrected field length you should use is 1,840 meters.
- **Model answer**: Based on the "Field Length Weight - Slope and Wind Corrections" table on page 103, here is the step-by-step calculation:

1.  **Find the Slope Corrected Field Length:**
    *   Go to the **SLOPE CORRECTION** table.
    *   Find the row for "Available Field Length (M)" of **2000**.
    *   Find the column for "Runway Slope (%)" under "Uphill" for **1.0**.
    *   The value at this intersection is **1820**.

2.  **Find the Wind Corrected Field Length:**
    *   Go to the **WIND CORRECTION** table.
    *   Use the slope-corrected length of 1820m. Find the closest row, which is **1800**.
    *   Find the column for "Wind Component (KT)" under "Tailwind" for **10**.
    *   The value at this intersection is **1520**.

The final slope and wind-corrected field length you should use is **1520 meters**.
- **Labelled pages**: 81
- **Returned pages**: 32, 61, 76, 102, 103
- **Answer correctness (YES/NO)**: NO
- **Page reference correctness (0–10)**: 0.00
### Q17

- **Question**: I need to check the crew oxygen. There are 3 of us, and the bottle temperature gauge reads 30°C. What is the minimum required pressure in PSI for our 114 Cu. Ft. cylinder?
- **Labelled answer**: For 3 crew members at a bottle temperature of 30°C, the minimum required pressure for the 114/115 Cu. Ft. cylinder is 690 PSI.
- **Model answer**: Based on the "Required Pressure (PSI) for 114/115 Cu. Ft. Cylinder" table on page 94, the minimum required pressure is **990 PSI**.

Here is how to find it:
1.  Locate the correct table: "Required Pressure (PSI) for 114/115 Cu. Ft. Cylinder".
2.  Find the row for the bottle temperature: Go down the "°C" column to **30**.
3.  Find the column for the number of crew: Go across the "NUMBER OF CREW USING OXYGEN" header to the column for **3**.
4.  The value at the intersection of this row and column is **990**.
- **Labelled pages**: 94
- **Returned pages**: 59, 94, 106, 123, 144
- **Answer correctness (YES/NO)**: NO
- **Page reference correctness (0–10)**: 2.00
### Q18

- **Question**: We're on an ILS approach. What three actions should I initiate as soon as the glideslope comes alive?
- **Labelled answer**: Based on the ILS Approach diagram and the Landing Procedure, as soon as the glideslope is "alive," you should initiate these three actions:

Call for "GEAR DOWN"

Call for "FLAPS 15"

Arm speed brake
- **Model answer**: Based on the ILS Approach diagram on page 52, the three actions to initiate when the glideslope comes alive are:

1.  **Gear down**
2.  **Flaps 15** (final flap for 1 engine)
3.  **Arm speedbrake**
- **Labelled pages**: 45, 52
- **Returned pages**: 4, 52, 64, 69, 76
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q19

- **Question**: What are the three available settings on the POSITION light switch located on the forward overhead panel?
- **Labelled answer**: Here are the three available settings on the POSITION Light switch:


STROBE & STEADY 


OFF 


STEADY
- **Model answer**: Based on the "Miscellaneous Exterior Lights" diagram on page 113, the three available settings on the POSITION light switch are:

*   **STROBE & STEADY**
*   **OFF**
*   **STEADY**
- **Labelled pages**: 113
- **Returned pages**: 112, 113, 114, 126, 131
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
### Q20

- **Question**: Looking at the components of the passenger entry door, what is the name of the bar that secures the emergency escape slide to the aircraft floor?
- **Labelled answer**: Based on the "Passenger Entry/Galley Service Doors" diagram in the manual, the bar that secures the emergency escape slide to the floor brackets is called the GIRT BAR.
- **Model answer**: Based on the diagram on page 123 titled "Passenger Entry/Galley Service Doors," the name of the bar that secures the emergency escape slide to the aircraft floor is the **GIRT BAR**.
- **Labelled pages**: 123
- **Returned pages**: 123, 134, 137, 138, 139
- **Answer correctness (YES/NO)**: YES
- **Page reference correctness (0–10)**: 2.00
