import { useSelector } from "react-redux";
import { RootState } from "../redux/store";

export default function FormPanel() {
  const form = useSelector((state: RootState) => state.interaction.form);
  const followups = useSelector(
    (state: RootState) => state.interaction.followups
  );
  const artifact_file = useSelector(
    (state: RootState) => state.interaction.artifact_file
  );

  const sentimentOptions = [
    { value: "positive", label: "Positive", icon: "😊" },
    { value: "neutral", label: "Neutral", icon: "😐" },
    { value: "negative", label: "Negative", icon: "😟" },
  ];

  // field renderer
  const Field = ({ label, value }: { label: string; value: any }) => {
    const renderValue = () => {
      if (!value) return "-";

      if (Array.isArray(value)) {
        return value
          .map((v) => {
            if (typeof v === "object") {
              return (
                v.medicine_name ||
                v.sample_name ||
                v.name ||
                JSON.stringify(v)
              );
            }
            return v;
          })
          .join(", ");
      }

      if (typeof value === "object") {
        return JSON.stringify(value);
      }

      return value;
    };

    return (
      <div className="flex justify-between py-2 border-b text-sm">
        <span className="text-gray-500">{label}</span>
        <span className="font-medium text-gray-800 text-right max-w-[60%]">
          {renderValue()}
        </span>
      </div>
    );
  };

  return (
    <div className="space-y-4">

      {/* main form card*/}
      <div className="bg-white rounded-xl shadow-sm border p-5 space-y-2">

        <Field label="HCP Name" value={form?.hcp_name} />
        <Field label="Interaction Type" value={form?.interaction_type} />
        <Field label="Date" value={form?.date} />
        <Field label="Time" value={form?.time} />
        <Field label="Attendees" value={form?.attendees} />
        <Field label="Topics Discussed" value={form?.topics_discussed} />
        <Field label="Materials Shared" value={form?.materials_shared} />

        {/* custome samples distributed field */}
        <div className="flex justify-between py-2 border-b text-sm">
          <span className="text-gray-500">Samples Distributed</span>

          <div className="text-right max-w-[60%]">
            {Array.isArray(form?.samples_distributed) &&
              form.samples_distributed.map((item: any, i: number) => (
                <div key={i} className="text-gray-800">
                  {typeof item === "string"
                    ? item
                    : `${item.medicine_name} - ${item.sample_name} (${item.quantity || "-"})`}
                </div>
              ))}

            {/* artifact PDF */}
            {artifact_file && (
              <button
                onClick={() => window.open(artifact_file, "_blank")}
                className="text-blue-600 text-xs hover:underline mt-1"
              >
                View / Download Report
              </button>
            )}
          </div>
        </div>

        <Field label="Outcomes" value={form?.outcomes} />
        <Field label="Followup Actions" value={form?.followup_actions} />

        {/* cutom sentiment component*/}
        <div className="py-3 border-b">
          <span className="text-gray-500 text-sm block mb-2">
            Observed / Inferred HCP Sentiment
          </span>

          <div className="flex gap-3">
            {sentimentOptions.map((opt) => {
              const isActive =
                (form?.sentiment || "").toLowerCase() === opt.value;

              return (
                <div
                  key={opt.value}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-sm transition
                    ${
                      isActive
                        ? "bg-blue-50 border-blue-400 text-blue-700"
                        : "bg-white text-gray-500 border-gray-200"
                    }
                  `}
                >
                  <span className="text-lg">{opt.icon}</span>
                  <span>{opt.label}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* folllowups component */}
      <div className="bg-blue-50 border border-blue-100 rounded-xl p-5">
        <h3 className="font-semibold text-blue-800 mb-2">
          AI Suggested Followups
        </h3>

        <ul className="space-y-2 text-sm text-blue-900">
          {followups?.length ? (
            followups.map((f: any, i: number) => (
              <li key={i} className="bg-white p-2 rounded-md shadow-sm">
                {typeof f === "string" ? f : f?.title || JSON.stringify(f)}
              </li>
            ))
          ) : (
            <li className="text-blue-500">No suggestions yet</li>
          )}
        </ul>
      </div>
    </div>
  );
}