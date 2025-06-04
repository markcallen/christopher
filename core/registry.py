AGENT_REGISTRY = {}


def agent(name):
    def decorator(cls):
        if not hasattr(cls, "description"):
            raise ValueError(
                f"Agent class {cls.__name__} must have a 'description' class variable"
            )
        AGENT_REGISTRY[name] = {"instance": cls(), "description": cls.description}
        return cls

    return decorator
