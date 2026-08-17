"""
Athena Core Orchestrator

Central coordinator for Athena.

Athena interprets the user's request and chooses
the appropriate tool.

Quantitative calculations are delegated to the
Quant Research Tool.
"""

from models.ollama_client import OllamaClient
from memory.conversation_memory import save_conversation
from core.fiona_router import route_task
from staff.employee_registry import get_model
from staff.prompt_builder import build_employee_prompt
from memory.retrieval import retrieve
from response.typesetter import typeset_response
from reasoning.parser import (
    parse_quant_request,
)

from reasoning.llm_parser import (
    QuantLLMParser,
)

from tools.quant_research import (
    QuantResearchTool,
)


QUANT_LANGUAGE = {
    "risk",
    "downside",
    "tail",
    "left tail",
    "left-tail",
    "var",
    "value at risk",
    "expected shortfall",
    "volatility",
    "drawdown",
    "sharpe",
    "sortino",
    "correlation",
    "covariance",
    "portfolio",
    "monte carlo",
    "simulation",
    "simulate",
    "stress",
    "scenario",
    "beta",
    "exposure",
    "hedge",
    "backtest",
    "backtesting",
    "returns",
}


QUANT_TASKS = {
    "risk_analysis",
    "simulation",
    "portfolio_analysis",
    "stress_test",
    "optimization",
}


class AthenaOrchestrator:

    def __init__(self):
        self.name = "Athena"

        self.llm = OllamaClient()

        self.quant_tool = QuantResearchTool()


    def process_request(
        self,
        message,
    ):
        """
        Main Athena reasoning loop.

        Fast path:
            deterministic parser

        Ambiguous quantitative language:
            LLM parser

        Quantitative execution:
            Quant Research Tool

        General conversation:
            Fiona routes to employee
        """

        baseline = parse_quant_request(
            message
        )

        request = baseline


        if self._needs_llm_parser(
            message,
            baseline,
        ):

            parser = QuantLLMParser()

            request = parser.parse(
                message
            )


        if request.task in QUANT_TASKS:

            return self.quant_tool.execute(
                request
            )


        return self._general_response(
            message
        )


    def _needs_llm_parser(
        self,
        message,
        baseline,
    ):
        """
        Use LLM parser only when deterministic parsing
        cannot classify quantitative language.
        """

        if baseline.task != "general_analysis":
            return False


        text = message.lower()


        return any(
            phrase in text
            for phrase in QUANT_LANGUAGE
        )


    def _general_response(
        self,
        message,
    ):
        """
        Athena's general conversation path.

        Fiona decides which employee should handle
        the request.

        The employee's professional profile is then
        loaded dynamically and used to build the
        runtime prompt for their current model.
        """

        decision = route_task(
            message
        )

        employee_id = decision[
            "employee"
        ]
        if employee_id == "kev":
            return self._memory_response(
                message=message,
                decision=decision,
            )

        model = get_model(
            employee_id
        )

        memories = retrieve(
            message,
            limit=5,
            scope=decision["memory_scope"],
        )

        memory_context = "\n\n".join(
            (
                f"Source: "
                f"{memory['metadata'].get('filename', 'unknown')}\n"
                f"Scope: "
                f"{memory['metadata'].get('scope', 'unknown')}\n\n"
                f"{memory['content']}"
            )
            for memory in memories
        )

        prompt = build_employee_prompt(
            employee_id=employee_id,
            task=message,
            memory_context=memory_context,
        )
           

        response = self.llm.generate(
            prompt,
            model=model,
        )

        response = typeset_response(
            response
        )

        save_conversation(
            user_message=message,
            assistant_response=response,
        )

        return response
    
    def _memory_response(
        self,
        message,
        decision,
    ):
        """
        Kev performs memory retrieval immediately.

        conversation_historian:
            searches conversation history

        document_retrieval_specialist:
            searches indexed documents

        memory_librarian:
            searches the requested memory scope
        """

        mode = decision.get(
            "mode",
            "memory_librarian",
        )

        requested_scope = decision.get(
            "memory_scope"
        )


        if mode == "conversation_historian":

            scope = "conversations"

        elif mode == "document_retrieval_specialist":

            # Document retrieval should not accidentally
            # search conversation history.
            scope = requested_scope

            if (
                not scope
                or scope == "conversations"
            ):
                scope = "school"

        else:

            scope = requested_scope


        memories = retrieve(
            message,
            limit=10,
            scope=scope,
        )


        # School is currently the broad indexed-document
        # scope, so use it as a fallback for document lookup.
        if (
            not memories
            and mode
                == "document_retrieval_specialist"
            and scope != "school"
        ):

            scope = "school"

            memories = retrieve(
                message,
                limit=10,
                scope=scope,
            )


        if not memories:

            if mode == "conversation_historian":

                return (
                    "I couldn't find a matching "
                    "conversation in memory."
                )

            if mode == "document_retrieval_specialist":

                return (
                    "I couldn't find a matching item "
                    "in the indexed documents."
                )

            return (
                "I couldn't find a matching memory."
            )


        memory_context = "\n\n".join(
            (
                f"Source: "
                f"{memory['metadata'].get('filename', 'unknown')}\n"
                f"Scope: "
                f"{memory['metadata'].get('scope', 'unknown')}\n\n"
                f"{memory['content']}"
            )
            for memory in memories
        )

        prompt = f"""
You are Fiona Gallagher, Chief of Staff for Athena.

Kev has ALREADY completed the requested retrieval.
The results are included below.

Do not say that you will ask Kev.
Do not say that you will route the request to Kev.
Do not say that Kev needs to check something later.
Do not claim that Athena cannot access information
that is present in the retrieved results.

Answer the user's request directly from the
retrieved evidence.

RETRIEVAL RESPONSE STYLE

If this is document retrieval:

- Begin with a concise direct answer.
- Identify the single most relevant source first.
- Explain briefly why that source is the best match.
- Then mention supporting sources only when useful.
- Do not dump every retrieved chunk by default.
- Quote or reproduce only the portions needed to answer.
- If several files contain essentially the same material,
  group them instead of listing them separately.
- Prefer a useful summary over a raw retrieval transcript.
- Offer deeper detail only when the user asks for it.

If this is conversation history:

- Summarize the relevant prior discussion.
- Focus on decisions, work completed, and next steps.
- Do not dump raw conversation transcripts unless requested.

Preserve source identity.
Do not call material "your notes", "your lecture",
or "your course materials" unless the metadata
actually establishes that.

If the retrieved evidence does not answer the
question, say that clearly rather than guessing.

Retrieval mode:
{mode}

Retrieval scope:
{scope}

Retrieved results:

{memory_context}

User request:

{message}
"""
    


        response = self.llm.generate(
            prompt,
            model="fiona",
        )

        response = typeset_response(
            response
        )


        save_conversation(
            user_message=message,
            assistant_response=response,
        )


        return response

def process_request(
    message,
):
    """
    Functional compatibility wrapper.
    """

    athena = AthenaOrchestrator()

    return athena.process_request(
        message
    )