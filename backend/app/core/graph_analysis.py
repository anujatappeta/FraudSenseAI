def generate_trust_graph(profile):
    """
    Generate trust graph nodes and links based on profile verification.
    """
    nodes = [
        {"id": "Profile", "label": "Profile"},
        {"id": "Resume Check", "label": "Resume Consistency"},
        {"id": "LinkedIn", "label": "LinkedIn Verified" if profile.get("linkedin_verified") else "LinkedIn Missing"},
        {"id": "GitHub", "label": "GitHub Verified" if profile.get("github_verified") else "GitHub Missing"},
        {"id": "Company Check", "label": "Company Verified" if profile.get("company_verified") else "Company Not Found"},
        {"id": "Certificate", "label": "Certificate Verified" if profile.get("certificate_verified") else "Certificate Missing"},
    ]

    links = [
        {"source": "Profile", "target": "Resume Check"},
        {"source": "Profile", "target": "LinkedIn"},
        {"source": "Profile", "target": "GitHub"},
        {"source": "Profile", "target": "Company Check"},
        {"source": "Profile", "target": "Certificate"},
    ]

    return {"nodes": nodes, "links": links}
