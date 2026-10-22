// Create a Text parameter RepoRoot containing your checkout path, without a trailing slash.
// Read-only import. Null company values stay null. No unlike metric aggregation.
let
    Base = Text.TrimEnd(RepoRoot, {"/", "\"}) & "/outputs/powerbi/",
    Load = (name as text, types as list) as table =>
        let
            Headers = Table.PromoteHeaders(Csv.Document(File.Contents(Base & name),
                [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
                [PromoteAllScalars=true]),
            EmptyAsNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue,
                List.Transform(types, each _{0}))
        in Table.TransformColumnTypes(EmptyAsNull, types, "en-US"),
    Groundwater = Load("Groundwater.csv", {{"state", type text}, {"recharge_bcm", type number}, {"extractable_bcm", type number}, {"extraction_bcm", type number}, {"stage_pct", type number}, {"year", Int64.Type}, {"source_id", type text}, {"evidence_type", type text}, {"scope", type text}, {"locator", type text}}),
    CompanyReports = Load("CompanyReports.csv", {{"observation_id", type text}, {"company", type text}, {"metric", type text}, {"value", type number}, {"unit", type text}, {"period", type text}, {"geography", type text}, {"scope", type text}, {"water_metric", type text}, {"energy_denominator", type text}, {"evidence_type", type text}, {"source_id", type text}, {"locator", type text}, {"confidence", type text}, {"confidence_basis", type text}, {"assurance", type text}, {"caveat", type text}}),
    LocationContext = Load("LocationContext.csv", {{"location_id", type text}, {"company", type text}, {"location", type text}, {"value", type number}, {"unit", type text}, {"period", type text}, {"water_metric", type text}, {"source_id", type text}, {"locator", type text}, {"confidence", type text}, {"scope", type text}, {"caveat", type text}, {"stress_region", type text}, {"stress_score", type number}, {"stress_label", type text}, {"stress_period", type text}, {"stress_source_id", type text}, {"stress_locator", type text}, {"match_scale", type text}, {"match_confidence", type text}, {"match_caveat", type text}}),
    Scenarios = Load("Scenarios.csv", {{"warning", type text}, {"name", type text}, {"year", Int64.Type}, {"demand_growth", type number}, {"efficiency_gain", type number}, {"it_mwh", type number}, {"facility_mwh", type number}, {"direct_l", type number}, {"indirect_l", type number}, {"total_l", type number}, {"carbon_kg", type number}, {"intensity_l_kwh_it", type number}, {"evidence_type", type text}, {"boundary", type text}}),
    Claims = Load("Claims.csv", {{"id", type text}, {"title", type text}, {"value", type number}, {"unit", type text}, {"period", type text}, {"geography", type text}, {"scope", type text}, {"evidence_type", type text}, {"source_id", type text}, {"locator", type text}, {"caveat", type text}, {"confidence", type text}, {"water_metric", type text}, {"energy_denominator", type text}}),
    Sources = Load("Sources.csv", {{"source_id", type text}, {"title", type text}, {"publisher", type text}, {"url", type text}, {"locator", type text}, {"scope", type text}, {"licence", type text}}),
    EvidenceStatus = Load("EvidenceStatus.csv", {{"topic", type text}, {"level", type text}, {"source_locator", type text}, {"caveat", type text}, {"missing", type text}})
in
    [Groundwater=Groundwater, CompanyReports=CompanyReports, LocationContext=LocationContext, Scenarios=Scenarios, Claims=Claims, Sources=Sources, EvidenceStatus=EvidenceStatus]
