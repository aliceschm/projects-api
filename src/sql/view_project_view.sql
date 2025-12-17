-- View to display all project details - NOT being used in API services

CREATE OR REPLACE VIEW portfolio.project_view AS
SELECT 
    p.id,
    p.updated_at,
    p.deploy_date,
    p.status,
    COALESCE(array_agg(DISTINCT s.id) FILTER (WHERE s.id IS NOT NULL), '{}')   AS stack_ids,
    COALESCE(array_agg(DISTINCT s.name) FILTER (WHERE s.name IS NOT NULL), '{}') AS stack_names,
    jsonb_object_agg(
        pd.lang,
        jsonb_build_object(
            'name',      pd.name,
            'about',     pd.about,
            'full_desc', pd.full_desc
        )
    ) AS translations
FROM portfolio.projects p
LEFT JOIN portfolio.project_desc pd 
    ON pd.project_id = p.id
LEFT JOIN portfolio.project_stack ps
    ON ps.project_id = p.id
LEFT JOIN portfolio.stacks s
    ON s.id = ps.stack_id
GROUP BY 
    p.id, 
    p.updated_at,
    p.status;
